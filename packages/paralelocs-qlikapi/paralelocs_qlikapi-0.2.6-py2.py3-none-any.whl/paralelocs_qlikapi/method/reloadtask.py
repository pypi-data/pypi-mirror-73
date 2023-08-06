
from paralelocs_qlikapi.method.base import DefaultMethods
import json

_TASK_TYPES = {
                'minutely':'* 0 0 0',
                'hourly'  :'0 * 0 0',
                'daily'   :'0 0 * 0',
                'weekly'  :'0 0 0 *',
                'monthly' :'0 0 0 0 *',
                'yearly'  :'0 0 0 0 0 *'
}

class Task(DefaultMethods):
    """
    Classe para trabalhar com o recurso APP da API do QLIK

    """

    def __init__(self,
                 auth= None,
                 session=None):
        super().__init__(auth=auth, session=session)
        self.resource = 'reloadtask'


    def create_event(self, appid, taskname, startdate, time, every='1', timeZone="America/Sao_paulo"):
        method = 'POST'
        resource = 'reloadtask/create'
        cron = str(_TASK_TYPES[time])
        incrementDescription = cron.replace('*', every)
        body = dict(
            task = self.create_task_dict(appid=appid, taskname=taskname),
            schemaEvents = self.create_schema_events_dict(taskname=str(time).capitalize(), startdate=startdate, timeZone=timeZone, incrementDescription= incrementDescription)
        )
        data = json.dumps(body)
        return self.send(method = method, resource= resource, data=data)

       
    def create_trigger(self, appid, taskname, triggername='Load sucessfully', tasks=[], **kwargs):
        """
            Tasks is a list of task with id
            tasks [{'id':'1212sdsad-asdsad-asd'}, {'id':'121212-dsad-asas'}]
        """
        method = 'POST'
        resource = 'reloadtask/create'

        body = dict(
            task = self.create_task_dict(appid=appid, taskname=taskname),
            compositeEvents = self.create_composite_events_dict(triggername=triggername, tasks=tasks)
        )
        data = json.dumps(body)
        return self.send(method = method, resource= resource, data=data)
        

    def create_composite_events_dict(self, triggername, tasks):
        compositeEvents = []
        compositeRules = []

        for task in tasks:
            _task = dict(
                        reloadTask= dict(id=task['id']),
                        ruleState = 1
                        )

            compositeRules.append(_task)
        union = dict(
                timeConstraint = dict(days=0, hours=0,minutes=360,seconds=0),
                compositeRules = compositeRules,
                name = triggername,
                enabled = True,
                eventType = 1
            )
        
        compositeEvents.append(union)

        return compositeEvents


    def create_task_dict(self, appid, taskname, taskSessionTimeout=1440, maxRetries=0, enable=True):
        body = dict(
            
                    app= dict(
                                id= appid,
                                ), 
                    name=taskname,
                    taskSessionTimeout= taskSessionTimeout,
                    maxRetries = maxRetries,
                    enable= enable
                    )
        return body

    def create_body_dict(self):

        body = dict(
            task = self.create_task_dict(),
            compositeEvents = self.create_composite_events_dict(),
            schemaEvents = self.create_schema_events_dict()
        )

        return body

    def create_schema_events_dict(self, taskname, startdate, expirationDate="9999-01-01T00:00:00.000", timeZone="America/New_York", incrementDescription="0 0 1 0"):
        schemaEvents = []
        schemaFilterDescription = ["* * - * * * * *"]

        body = dict(
            timeZone = timeZone,
            daylightSavingTime = 0,
            startDate = startdate,#"2017-01-11T12:05:46.000",
            expirationDate = expirationDate,
            schemaFilterDescription = schemaFilterDescription,
            incrementDescription = incrementDescription,   # 1 2 3 4 : 1 - minute, 2 - hours, 3 - days, 4 - weekly
            incrementOption = 2,
            name = taskname,
            eventType = 0,
            enabled = True
        )
        
        schemaEvents.append(body)

        return schemaEvents



    def reload(self, name):
        app = self.search(name=name)
        app = app['content'][0]
        appid = app['id']
        resource = f'app/{appid}/reload'
        method = 'POST'
        data = ''
        
        return self.send(method = method, resource= resource, data=data)