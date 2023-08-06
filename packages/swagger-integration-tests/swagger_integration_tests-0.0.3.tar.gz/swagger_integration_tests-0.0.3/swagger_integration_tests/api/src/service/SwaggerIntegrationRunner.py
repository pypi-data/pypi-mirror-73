from swagger_integration_tests.api.src.service import SwaggerIntegrationTests

class SwaggerIntegrationRunner(SwaggerIntegrationTests.SwaggerIntegrationTests):

    _0_API_KEY = 0
    _1_COMMAND = 1
    _0_ARGUMENT = 2
    _1_ARGUMENT = 3
    _2_ARGUMENT = 4

    COMMAND_RUN = 'run'

    def handleCommandList(self,commandList):
        commandList = commandList.copy()
        globals = self.globals
        if commandList :
            apiKey = commandList[self._0_API_KEY]
            if len(commandList) > self._1_COMMAND and commandList[self._1_COMMAND] :
                try :
                    if len(commandList) > self._0_ARGUMENT :
                        response = self.commandSet[commandList[self._1_COMMAND]](commandList[self._0_ARGUMENT:])
                    else :
                        response = self.commandSet[commandList[self._1_COMMAND]]([])
                    globals.debug(f'response = {response}')
                    return response
                except Exception as exception :
                    print(f'{globals.ERROR}Failed to execute command: "{commandList[self._1_COMMAND]}". Cause: {str(exception)}')
                    return
            else :
                print(f'Missing command: {list(self.commandSet.keys())}')
        else :
            print(f'Missing api key in command line')


    def __init__(self,*args,**kwargs):
        SwaggerIntegrationTests.SwaggerIntegrationTests.__init__(self,*args,**kwargs)
        self.commandSet = {
            self.COMMAND_RUN : self.run
        }

    def repository(self,logName,logContent):
        extension = 'yml'
        logPath = f'{self.globals.apiPath}{self.globals.baseApiPath}repository\\'
        with open(f'{logPath}{logName}.{extension}', 'w+', encoding="utf-8") as logFile :
            logFile.write(logContent)

    def run(self,tagList):
        testSet = self.getTestSet(tagList)
        self.runTestSet(testSet)
        return f'{self.__class__.__name__} process finished.'

    def getTestSet(self,tagList):
        globals = self.globals
        completeTestSet = globals.getPathTreeFromPath(self.integrationPath)
        for key in completeTestSet.keys() :
            completeTestSet[key] = self.globals.getFileNameList(f'{self.integrationPath}{key}{self.globals.BACK_SLASH}')
        if tagList :
            return self.buildTestSet(tagList,completeTestSet)
        else :
            return completeTestSet

    def buildTestSet(self,tagList,completeTestSet):
        testSet = {}
        for tag in tagList :
            testSet[tag] = completeTestSet[tag]
        return testSet
