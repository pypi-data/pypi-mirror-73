import yaml
import datetime
import os
import time
import socket
from hashlib import sha224
from collections import OrderedDict, defaultdict
import glob
import logging
import io
import re
import click
import urllib.parse


from bravado.client import SwaggerClient

try:
    import io
except:
    from io import StringIO

try:
    import urlparse # type: ignore
except ImportError:
    import urllib.parse as urlparse# type: ignore

from typing import NewType, Dict

TaskDict = NewType('TaskDict', Dict)
TaskData = NewType('TaskData', Dict)

import pymysql
import peewee # type: ignore
from playhouse.db_url import connect # type: ignore
from playhouse.shortcuts import model_to_dict, dict_to_model # type: ignore

sleep_multiplier = 1
n_failed_retries = int(os.environ.get('DQUEUE_FAILED_N_RETRY','20'))

logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler=logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s %(levelname)8s %(name)s | %(message)s')
handler.setFormatter(formatter)

def log(*args,**kwargs):
    severity=kwargs.get('severity','warning').upper()
    logger.log(getattr(logging,severity)," ".join([repr(arg) for arg in list(args)+list(kwargs.items())]))


class Empty(Exception):
    pass

class CurrentTaskUnfinished(Exception):
    pass

class TaskStolen(Exception):
    pass


def connect_db():
    return connect(os.environ.get("DQUEUE_DATABASE_URL","mysql+pool://root@localhost/dqueue?max_connections=42&stale_timeout=8001.2"))

try:
    db=connect_db()
    logger.info(f"successfully connected to db: {db}")
except Exception as e:
    logger.warning("unable to connect to DB: %s", repr(e))

    

class TaskEntry(peewee.Model):
    queue = peewee.CharField(default="default")

    key = peewee.CharField(primary_key=True)
    state = peewee.CharField()
    worker_id = peewee.CharField()
    entry = peewee.TextField()

    created = peewee.DateTimeField()
    modified = peewee.DateTimeField()

    class Meta:
        database = db

class TaskHistory(peewee.Model):
    queue = peewee.CharField(default="default")

    key = peewee.CharField()
    state = peewee.CharField()
    worker_id = peewee.CharField()

    timestamp = peewee.DateTimeField()
    message = peewee.CharField()

    class Meta:
        database = db

try:
    db.create_tables([TaskEntry,TaskHistory])
    has_mysql = True
except peewee.OperationalError:
    has_mysql = False
except Exception:
    has_mysql = False

class Task:
    def __init__(self,task_data,execution_info=None, submission_data=None, depends_on=None):
        self.task_data=task_data
        self.submission_info=self.construct_submission_info()
        self.depends_on=depends_on

        if submission_data is not None:
            self.submission_info.update(submission_data)

        self.execution_info=execution_info

    def construct_submission_info(self):
        return dict(
            time=time.time(),
            utc=time.strftime("%Y%m%d-%H%M%S"),
            hostname=socket.gethostname(),
            fqdn=socket.getfqdn(),
            pid=os.getpid(),
        )
    
    @property
    def as_dict(self):
        return dict(
                submission_info=self.submission_info,
                task_data=self.task_data,
                execution_info=self.execution_info,
                depends_on=self.depends_on,
            )

    def serialize(self):
        return yaml.dump(self.as_dict,
            default_flow_style=False, default_style=''
        )


    @classmethod
    def from_entry(cls,entry):
        if isinstance(entry, str):
            task_dict = yaml.load(io.StringIO(entry) , Loader=yaml.Loader )
        else:
            task_dict = entry

        print(task_dict['task_data'].keys())

        self=cls(task_dict['task_data'])
        self.depends_on=task_dict.get('depends_on', [])
        self.submission_info=task_dict['submission_info']

        return self

        


    @property
    def key(self):
        return self.get_key(True)

    def get_key(self,key=True):
        components = []

        task_data_string = yaml.dump(order_task_data(self.task_data), encoding='utf-8')

        logger.debug("task data: %s", self.task_data)
        logger.debug("task data string: %s", task_data_string)

        components.append(sha224(task_data_string).hexdigest()[:8])
        #log("encoding: "+repr(components))
        #log(task_data_string)
        #log("encoding: "+repr(components),severity="debug")
        #log(task_data_string,severity="debug")

        if not key:
            components.append("%.14lg"%self.submission_info['time'])
            components.append(self.submission_info['utc'])

            components.append(sha224(str(OrderedDict(sorted(self.submission_info.items()))).encode('utf-8')).hexdigest()[:8])

        key = "_".join(components)

        logger.warning("generating key %s from %s", key, task_data_string)

        return key

    def __repr__(self):
        return "[{}: {}]".format(self.__class__.__name__,self.task_data)

    def filename_instance(self):
        return "unset"

def makedir_if_neccessary(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != 17: raise

def list_queues(pattern=None):
    if pattern is None:
        return [ Queue(task_entry.queue) for task_entry in 
                TaskEntry.select(TaskEntry.queue).distinct() ]
    else:
        return [ Queue(task_entry.queue) for task_entry in 
                TaskEntry.select(TaskEntry.queue).where(TaskEntry.queue % pattern).distinct(TaskEntry.queue) ]


def order_task_data(d):
    if isinstance(d, dict) or isinstance(d, OrderedDict) or isinstance(d, defaultdict):
        return OrderedDict({
                k:order_task_data(v) for k, v in sorted(d.items())
            })

    return d


class Queue:
    def list_queues(self, pattern=None):
        return list_queues(pattern)

    def __init__(self,queue="default", worker_id=None):
        ""
        self.logger = logging.getLogger(repr(self))

        if worker_id is None:
            self.worker_id=self.get_worker_id()
        else:
            self.worker_id=worker_id

        self.queue=queue
        self.current_task=None
        self.current_task_status=None

    def find_task_instances(self,task,klist=None):
        ""
        log("find_task_instances for",task.key,"in",self.queue)
        if klist is None:
            klist=["waiting", "running", "done", "failed", "locked"]

        instances_for_key=[
                dict(task_entry=task_entry) for task_entry in TaskEntry.select().where(TaskEntry.state << klist, TaskEntry.key==task.key, TaskEntry.queue==self.queue)
            ]

        log("found task instances for",task.key,"N == ",len(instances_for_key))
        for i in instances_for_key:
            i['state'] = i['task_entry'].state
            log(i['state'], i['task_entry'])

        return instances_for_key
    
    def try_to_unlock(self,task):
        ""
        dependency_states=self.find_dependecies_states(task)
        

        if all([d['state']=="done" for d in dependency_states]):
            self.log_task("task dependencies complete: unlocking",task,"locked")
            log("dependecies complete, will unlock", task)
            self.move_task("locked", "waiting", task)
            return dict(state="waiting", key=task.key)

        if any([d['state']=="failed" for d in dependency_states]):
            log("dependecies complete, will unlock", task)
            self.log_task("task dependencies failed: unlocking to fail",task,"failed")
            self.move_task("locked", "failed", task)
            return dict(state="failed", key=task.key)

        if not any([d['state'] in ["running","waiting","locked","incomplete"] for d in dependency_states]):
            log("dependecies incomplete, but nothing will come of this anymore, will unlock", task)
            #self.log_task("task dependencies INcomplete: unlocking",task,"locked")

            from collections import defaultdict
            dd=defaultdict(int)
            for d in dependency_states:
                dd[d['state']]+=1

            self.log_task("task dependencies INcomplete: "+repr(dict(dd)),task,"locked")
           # self.move_task("locked", "waiting", task)
          #  return dict(state="waiting", key=task.key)

        log("task still locked", task.key)
        return dict(state="locked",key=task.key)
    
    
    def select_task_entry(self,key):
        ""

        r=TaskEntry.select().where(
                         TaskEntry.key==key,
                        ).execute()
        assert len(r)==1
        return r[0]
    
    def put(self, task_data: TaskData, submission_data=None, depends_on=None) -> TaskDict:
        logger.info("putting in queue task_data %s", task_data)

        assert depends_on is None or type(depends_on) in [list, tuple]

        task=Task(task_data,submission_data=submission_data,depends_on=depends_on)

        ntry_race=10
        retry_sleep_race=2
        while ntry_race>0:
            instances_for_key=self.find_task_instances(task)
            if len(instances_for_key)<=1:
                break
            log("found instances for key:",instances_for_key)
            log("found unexpected number of instances for key:",len(instances_for_key))
            log("sleeping for",retry_sleep_race,"attempt",ntry_race)
            time.sleep(retry_sleep_race)
            ntry_race-=1

        if len(instances_for_key)>1:
            raise Exception("probably race condition, multiple task instances:",instances_for_key)


        if len(instances_for_key) == 1:
            instance_for_key=instances_for_key[0]
        else:
            instance_for_key=None

        if instance_for_key is not None:
            log("found existing instance(s) for this key, no need to put:",instances_for_key)
            self.log_task("task already found",task,instance_for_key['state'])
            d = model_to_dict(instance_for_key['task_entry'])
            log("task entry:", d)
            return d

        if depends_on is None:
            self.insert_task_entry(task,"waiting")
            log("task inserted as waiting")
        else:
            self.insert_task_entry(task,"locked")
            log("task inserted as locked")

        instance_for_key=self.find_task_instances(task)[0]
        recovered_task=Task.from_entry(instance_for_key['task_entry'].entry)

        if recovered_task.key != task.key:
            log("inconsitent storage:")
            log("stored:",task.filename_instance)
            log("recovered:", recovered_task.filename_instance)
    
            #nfn=self.queue_dir("conflict") + "/put_original_" + task.filename_instance
            #open(nfn, "w").write(task.serialize())
        
            #nfn=self.queue_dir("conflict") + "/put_recovered_" + recovered_task.filename_instance
            #open(nfn, "w").write(recovered_task.serialize())
            
            #nfn=self.queue_dir("conflict") + "/put_stored_" + os.path.basename(fn)
            #open(nfn, "w").write(open(fn).read())

            raise Exception("Inconsistent storage")

        log("successfully put in queue:",instance_for_key['task_entry'].entry)

        #return dict(state="submitted", task_entry=instance_for_key['task_entry'].entry)
        d = model_to_dict(instance_for_key['task_entry'])
        d['state'] = 'submitted'
        return d

    def get(self):
        ""
        if self.current_task is not None:
            raise CurrentTaskUnfinished(self.current_task)

       # tasks=self.list("waiting")
       # task=tasks[-1]
       # self.current_task = Task.from_entry(task['task_entry'].entry)

    
        r=TaskEntry.update({
                        TaskEntry.state:"running",
                        TaskEntry.worker_id:self.worker_id,
                        TaskEntry.modified:datetime.datetime.now(),
                    })\
                    .order_by(TaskEntry.created)\
                    .where( (TaskEntry.state=="waiting") & (TaskEntry.queue==self.queue) ).limit(1).execute()

        if r==0:
            self.try_all_locked()
            raise Empty()

        entries=TaskEntry.select().where(TaskEntry.worker_id==self.worker_id,TaskEntry.state=="running").order_by(TaskEntry.modified.desc()).limit(1).execute()
        if len(entries)>1:
            raise Exception(f"several tasks ({len(entries)}) are running for this worker: impossible!")

        entry=entries[0]
        self.current_task=Task.from_entry(entry.entry)
        self.current_task_stored_key=self.current_task.key

        if self.current_task.key != entry.key:
            logger.error("current task key computed now does not match that found in record")
            logger.error("current task key: %s task: %s", self.current_task.key, self.current_task)
            logger.error("fetched task key: %s entry: %s", entry.key, entry)

        log(self.current_task.key)
        

        if self.current_task.key != entry.key:
            log("inconsitent storage:")
            log(">>>> stored:", entry)
            log(">>>> recovered:", self.current_task)

            #fn=self.queue_dir("conflict") + "/get_stored_" + self.current_task.filename_instance
            #open(fn, "w").write(self.current_task.serialize())
        
            #fn=self.queue_dir("conflict") + "/get_recovered_" + task_name
            #open(fn, "w").write(open(self.queue_dir("waiting")+"/"+task_name).read())

            raise Exception("Inconsistent storage")


        log("task is running",self.current_task)
        self.current_task_status = "running"

        self.log_task("task started")

        log('task',self.current_task.submission_info)

        return self.current_task

    def clear_task_history(self):
        ""
        print('this is very descructive')
        TaskHistory.delete().execute()

    def move_task(self, fromk, tok, task, update_entry=False):
        ""

        extra = {}
        if update_entry:
            extra = {TaskEntry.entry: self.current_task.serialize()}

        r=TaskEntry.update({
                        TaskEntry.state:tok,
                        TaskEntry.worker_id:self.worker_id,
                        TaskEntry.modified:datetime.datetime.now(),
                        **extra
                    })\
                    .where(TaskEntry.state==fromk, TaskEntry.key==task.key).execute()

    def purge(self):
        ""
        nentries=TaskEntry.delete().execute()
        log("deleted %i"%nentries)

        return nentries

    
    def try_all_locked(self):
        ""
        r=[]
        for task_key in self.list("locked"):
            task_entry=self.select_task_entry(task_key)
            log("trying to unlock", task_entry.key)
            #log("trying to unlock", task_key,task_entry,task_entry.key,task_entry.entry)
            r.append(self.try_to_unlock(Task.from_entry(task_entry.entry)))
        return r
    
    def remember(self,task_data,submission_data=None):
        ""
        task=Task(task_data,submission_data=submission_data)
        #nfn=self.queue_dir("problem") + "/"+task.filename_instance
        #open(nfn, "w").write(task.serialize())
            

    def insert_task_entry(self,task,state):
        self.log_task("task created",task,state)

        log("to insert_task_entry: ", dict(
             queue=self.queue,
             key=task.key,
             state=state,
             worker_id=self.worker_id,
             entry=task.serialize(),
             created=datetime.datetime.now(),
             modified=datetime.datetime.now(),
        ))

        try:
            TaskEntry.insert(
                             queue=self.queue,
                             key=task.key,
                             state=state,
                             worker_id=self.worker_id,
                             entry=task.serialize(),
                             created=datetime.datetime.now(),
                             modified=datetime.datetime.now(),
                            ).execute()
        except (pymysql.err.IntegrityError, peewee.IntegrityError) as e:
            log("task already inserted, reasserting the queue to",self.queue)

            # deadlock
            TaskEntry.update(
                                queue=self.queue,
                            ).where(
                                TaskEntry.key == task.key,
                            ).execute()


    def find_dependecies_states(self,task):
        if task.depends_on is None:
            raise Exception("can not inspect dependecies in an independent task!")

        log("find_dependecies_states for",task.key)

        dependencies=[]
        for i_dep,dependency in enumerate(task.depends_on):
            dependency_task=Task(dependency)

            print(("task",task.key,"depends on task",dependency_task.key,i_dep,"/",len(task.depends_on)))
            dependency_instances=self.find_task_instances(dependency_task)
            print(("task instances for",dependency_task.key,len(dependency_instances)))

            dependencies.append(dict(states=[]))

            for i_i,i in enumerate(dependency_instances):
                # if i['state']=="done"]) == 0:
                #log("dependency incomplete")
                dependencies[-1]['states'].append(i['state'])
                dependencies[-1]['task']=dependency_task
                print(("task instance for",dependency_task.key,"is",i['state'],"from",i_i,"/",len(dependency_instances)))

            if len(dependencies[-1]['states'])==0:
                print(("job dependencies do not exist, expecting %s"%dependency_task.key))
                #print(dependency_task.serialize())
                raise Exception("job dependencies do not exist, expecting %s"%dependency_task.key)

            if 'done' in dependencies[-1]['states']:
                dependencies[-1]['state']='done'
            elif 'failed' in dependencies[-1]['states']:
                dependencies[-1]['state']='failed'
            else:
                dependencies[-1]['state']='incomplete'
            
            try:
                log("dependency:",dependencies[-1]['state'],dependencies[-1]['states'], dependencies[-1]['task'].key, dependency_instances[0])
            except KeyError:
                log("problematic dependency:",dependencies[-1])
                raise Exception("problematic dependency:",dependencies[-1])
            #log("dependency:",dependencies[-1]['state'],dependencies[-1]['states'], dependency, dependency_instances)

        return dependencies




    def task_locked(self,depends_on):
        ""
        log("locking task",self.current_task)
        self.log_task("task to lock...",state="locked")
        if self.current_task is None:
            raise Exception("task must be available to lock")

        self.current_task.depends_on=depends_on
        serialized=self.current_task.serialize()

        self.log_task("task to lock: serialized to %i"%len(serialized),state="locked")

        n_tries_left=10
        retry_delay=2
        while n_tries_left>0:
            try:

                self.move_task('running', 'locked', self.current_task, update_entry=True)

               # r=TaskEntry.update({
               #             TaskEntry.state:"locked",
               #             TaskEntry.entry:serialized,
               #         }).where(
               #             TaskEntry.key==self.current_task.key,
               #             TaskEntry.state=="running",
               #          ).execute()
            except Exception as e:
                log('failed to lock:',repr(e))
                self.log_task("task to failed lock: %s; serialized to %i"%(repr(e),len(serialized)),state="failed_to_lock")
                time.sleep(retry_delay)
                if n_tries_left==1:
                    raise
                n_tries_left-=1
            else:
                break
        
        self.log_task("task locked from "+self.current_task_status,state="locked")

        self.current_task_status="locked"
        self.current_task=None


    def task_done(self):
        log("task done, closing:",self.current_task.key,self.current_task)
        log("task done, stored key:",self.current_task_stored_key)

        self.log_task("task to register done")

        r=TaskEntry.update({
                    TaskEntry.state:"done",
                    TaskEntry.entry:self.current_task.serialize(),
                    TaskEntry.modified:datetime.datetime.now(),
                }).where(TaskEntry.key==self.current_task.key).execute()

        if self.current_task_stored_key != self.current_task.key:
            r=TaskEntry.update({
                        TaskEntry.state:"done",
                        TaskEntry.entry:self.current_task.serialize(),
                        TaskEntry.modified:datetime.datetime.now(),
                    }).where(TaskEntry.key==self.current_task_stored_key).execute()


        self.current_task_status="done"

        self.log_task("task done")
        log('task registered done',self.current_task.key)

        self.current_task=None


    def task_failed(self,update=lambda x:None):
        update(self.current_task)

        task= self.current_task

        self.log_task("task failed",self.current_task,"failed")
        
        history=[model_to_dict(en) for en in TaskHistory.select().where(TaskHistory.key==task.key).order_by(TaskHistory.id.desc()).execute()]
        n_failed = len([he for he in history if he['state'] == "failed"])

        self.log_task("task failed %i times already"%n_failed,task,"failed")
        if n_failed < n_failed_retries:
            next_state = "waiting"
            self.log_task("task failure forgiven, to waiting",task,"waiting")
            time.sleep( (5+2**int(n_failed/2))*sleep_multiplier )
        else:
            next_state = "failed"
            self.log_task("task failure permanent",task,"waiting")

        r=TaskEntry.update({
                    TaskEntry.state:next_state,
                    TaskEntry.entry:self.current_task.serialize(),
                    TaskEntry.modified:datetime.datetime.now(),
                }).where(TaskEntry.key==self.current_task.key).execute()

        self.current_task_status = next_state
        self.current_task = None


    def wipe(self,wipe_from=["waiting"]):
        for fromk in wipe_from:
            for key in self.list(fromk):
                log("removing",fromk + "/" + key)
                TaskEntry.delete().where(TaskEntry.key==key).execute()
        
    @property
    def info(self):
        ""
        r={}
        for kind in "waiting","running","done","failed","locked":
            r[kind]=len(self.list(kind))
        return r

    def show(self):
        ""
        r=""
        for kind in "waiting","running","done","failed","locked":
            r+="\n= "+kind+"\n"
            for task_entry in TaskEntry.select().where(TaskEntry.state==kind, TaskEntry.queue==self.queue):
                r+=" - "+repr(model_to_dict(task_entry))+"\n"
        return r


    def watch(self,delay=1):
        """"""
        while True:
            log(self.info)
            time.sleep(delay)

    def get_worker_id(self):
        ""
        d=dict(
            time=time.time(),
            utc=time.strftime("%Y%m%d-%H%M%S"),
            hostname=socket.gethostname(),
            fqdn=socket.getfqdn(),
            pid=os.getpid(),
        )
        return "{fqdn}.{pid}".format(**d)


    def log_task(self, message, task=None, state=None, task_key=None):
        ""

        if task_key is not None:
            key=task_key
        else:
            if task is None:
                task=self.current_task

            task_key = task.key

        if state is None:
            state="undefined"

        return TaskHistory.insert(
                             queue=self.queue,
                             key=task_key,
                             state=state,
                             worker_id=self.worker_id,
                             timestamp=datetime.datetime.now(),
                             message=message,
                        ).execute()

    def list(self,kind=None,kinds=None,fullpath=False):
        ""
        if kinds is None:
            kinds=["waiting"]
        if kind is not None:
            kinds=[kind]

        kind_jobs = []

        for kind in kinds:
            for task_entry in TaskEntry.select().where(TaskEntry.state==kind, TaskEntry.queue==self.queue):
                kind_jobs.append(task_entry.key)
        return kind_jobs


