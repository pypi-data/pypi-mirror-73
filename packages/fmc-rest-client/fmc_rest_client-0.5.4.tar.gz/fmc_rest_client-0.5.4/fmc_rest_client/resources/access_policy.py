from fmc_rest_client.core.base_resources import *

"""
{
  "type": "AccessPolicy",
  "name": "AccessPolicy1",
  "description": "policy to test FMC implementation",
  "defaultAction": {
    "type": "AccessPolicyDefaultAction",
    "logBegin": "false",
    "logEnd": "false",
    "sendEventsToFMC": "false",
    "action": "3"
  }
}
"""
class AccessPolicy(PolicyResource):
    def __init__(self, name=None, default_action='TRUST', desc=None):
        super().__init__(name)
        self.name = name
        self.description = desc
        self.defaultAction = AccessPolicyDefaultAction(default_action)


class AccessPolicyDefaultAction(BaseContainedResource):
    def __init__(self, action='TRUST', log_begin=True, log_end=False):
        super()
        self.logBegin = log_begin
        self.logEnd = log_end
        self.sendEventsToFMC = False
        self.action = action

class AccessRuleMetadata(Metadata):
    def __init__(self, ruleIndex=-1, accessPolicy:ReferenceType=None, domain:ReferenceType=None, readOnly: ReadOnly=None):
        super().__init__(domain, readOnly)
        if accessPolicy:
            self.accessPolicy = accessPolicy
        else: #set so that json_load can find the type
            self.accessPolicy = ReferenceType(None)
        self.section = 'Mandatory'
        self.category = None
        self.ruleIndex = ruleIndex

    
"""
{
  "action": "ALLOW",
  "enabled": true,
  "type": "AccessRule",
  "name": "Rule1",
  "sendEventsToFMC": false,
  "logFiles": false,
  "logBegin": false,
  "logEnd": false,
  "variableSet": {
    "name": "Default Set",
    "id": "VariableSetUUID",
    "type": "VariableSet"
  }
}

"""
class AccessRule(ContainedPolicyResource):
    bulk_operations = ['POST']

    def __init__(self, name=None, container=None, action='ALLOW'):
        super().__init__(name, container)
        self.name = name
        self.action = action 
        self.sendEventsToFMC = False
        self.logBegin = False
        self.logEnd = False
        self.logFiles = False
        self.enabled = True
        self.enableSyslog = False
        self.syslogSeverity = None
        self.syslogConfig = None
        self.snmpConfig = None
        self.users = { 'objects': [] }
        self.newComments = []
        self.sourceZones = { 'objects': [] }
        self.destinationZones = { 'objects': [] }
        self.sourceNetworks = { 'objects': [] , 'literals': [] }
        self.destinationNetworks = { 'objects': [], 'literals': [] }
        self.urls = { 'urlCategoriesWithReputation': [] , 'objects': [] , 'literals': [] }
        self.vlanTags = { 'objects': [] , 'literals': [] }
        self.sourcePorts = { 'objects':  [] , 'literals': [] }
        self.destinationPorts = { 'objects': [] , 'literals': [] }
        self.sourceSecurityGroupTags = { 'objects': [] , 'literals': [] }
        self.destinationSecurityGroupTags = { 'objects': [] , 'literals': [] }
        self.applications = { 'inlineApplicationFilters': [], 'applicationFilters': [], 'applications': [] }
        self.ipsPolicy = None
        self.filePolicy = None
        self.variableSet = None
        self.commentHistoryList = []
        self.newComments = []
        self.metadata = AccessRuleMetadata()

    def _generate_queries(self, bulk_limit=1000, **kwargs):
        if 'section' in kwargs.keys() and kwargs['section'] is not None:
            kwargs.pop('category', None)
        if 'insertBefore' in kwargs.keys() and kwargs['insertBefore'] is not None:
            kwargs.pop('insertAfter', None)
        queries, kwargs = super()._generate_queries(bulk_limit, **kwargs)
        if 'insertBefore' in kwargs.keys() and kwargs['insertBefore'] is not None:
            kwargs['insertBefore'] = str(int(kwargs['insertBefore']) + bulk_limit)
        if 'insertAfter' in kwargs.keys() and kwargs['insertAfter'] is not None:
            kwargs['insertAfter'] = str(int(kwargs['insertAfter']) + bulk_limit)
        return queries, kwargs

    def json_load(self, json):
        super().json_load(json)
        if self.metadata.accessPolicy.id:
            self.container = AccessPolicy()
            self.container.id = self.metadata.accessPolicy.id

class IntrusionPolicy(PolicyResource):

    def __init__(self, name=None):
        super().__init__(name)

class FilePolicy(PolicyResource):

    def __init__(self, name=None):
        super().__init__(name)

class SNMPAlert(PolicyResource):

    def __init__(self, name=None):
        super().__init__(name)

class SyslogAlert(PolicyResource):

    def __init__(self, name=None):
        super().__init__(name)
