#!/usr/bin/env python

## Program:   PypeS
## Module:    $RCSfile: pypescript.py,v $
## Language:  Python
## Date:      $Date: 2006/05/26 12:36:30 $
## Version:   $Revision: 1.18 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.


import sys
import string
import os.path

class pypeMember(object):

    def __init__(self,memberName,optionName,memberType,memberLength,memberDoc='',memberIO=''):

        self.MemberName = memberName
        self.OptionName = optionName
        self.MemberType = memberType
        self.MemberLength = memberLength
        self.MemberDoc = memberDoc
        self.MemberIO = memberIO
        self.MemberPipe = ''
        self.MemberValue = None
        self.ExplicitPipe = ''
        self.AutoPipe = 1
        self.Pushed = 0
    
class pypeScript(object):
    
    def __init__(self):

        self.BuiltinOptionTypes = ['int','str','float']

        self.InputStream = sys.stdin
        self.OutputStream = sys.stdout

        self.ScriptName = ''
        self.ScriptDoc = ''
        self.Arguments = []
        self.InputMembers = []
        self.OutputMembers = []
        self.Id = 0
        self.Self = self

        idMember = pypeMember('Id','id','int',1,'script id')
        idMember.AutoPipe = 0
        self.InputMembers.append(idMember)
        self.OutputMembers.append(idMember)
        selfMember = pypeMember('Self','handle','self',1,'handle to self')
        selfMember.AutoPipe = 0
        self.InputMembers.append(selfMember)
        self.OutputMembers.append(selfMember)

        self.ExitOnError = 1
        self.LogOn = 1

        self.Progress = 0
                              
    def PrintLog(self,logMessage,indent=0):
        if not self.LogOn:
            return
        indentUnit = '    '
        indentation = ''
        for i in range(indent):
            indentation = indentation + indentUnit
        self.OutputStream.write(indentation + logMessage + '\n')

    def PrintError(self,errorMessage):
        self.OutputStream.write(errorMessage + '\n')
        if self.ExitOnError:
          self.Exit()
        else:
          raise RuntimeError
    
    def Exit(self):
        sys.exit()

    def OutputText(self,text):
        self.OutputStream.write(text)

    def OutputProgress(self,progress,percentStep):
        if int(100 * progress)/percentStep == int(100 * self.Progress)/percentStep:
            return
        self.Progress = progress
        self.OutputStream.write('\r')
        self.OutputStream.write('Progress: '+str(int(100 * self.Progress))+'%')
        self.OutputStream.flush()
 
    def EndProgress(self):
        self.OutputStream.write('\n')
        
    def InputText(self,prompt='',validator=None):
        self.OutputText(prompt)
        text = self.InputStream.readline().rstrip('\n')
        if validator:
            while not validator(text):
                self.OutputText(prompt)
                text = self.InputStream.readline().rstrip('\n')
        return text

    def PrintMembers(self,members):
        for memberEntry in members:
            memberName  = memberEntry.MemberName
            memberType = memberEntry.MemberType       
            memberPipe = memberEntry.MemberPipe
            memberValue = self.__getattribute__(memberName)
##            if memberPipe:
##                self.__getattribute__("PrintLog")(memberName+' = '+memberPipe,1)
            if memberName == 'Self':
                pass
            elif (memberType in self.BuiltinOptionTypes) or (memberType == 'list'):
                self.__getattribute__("PrintLog")(memberName+' = '+str(memberValue),1)
            elif memberValue:
                self.__getattribute__("PrintLog")(memberName+' = '+memberType,1)
            else:
                self.__getattribute__("PrintLog")(memberName+' = '+str(memberValue),1)
                           
    def PrintInputMembers(self):
        self.PrintLog("Input " + self.ScriptName + " members:")
        self.PrintMembers(self.InputMembers)

    def PrintOutputMembers(self):
        self.PrintLog("Output " + self.ScriptName + " members:")
        self.PrintMembers(self.OutputMembers)

    def ConvertToPypeMembers(self,members):
        pypeMembers = []
        for member in members:
            if type(member) == pypeMember:
                pypeMembers.append(member)
            elif type(member) == list:
                pypeMembers.append(pypeMember(*member))
        return pypeMembers

    def SetInputMembers(self,membersToAppend):
        pypeMembersToAppend = self.ConvertToPypeMembers(membersToAppend)
        for member in pypeMembersToAppend:
            self.InputMembers.append(member)
            if member.MemberIO:
                filenameMember = pypeMember(self.GetIOInputFileNameMember(member.MemberName),self.GetIOFileNameOption(member.OptionName),'str',1,'filename for the default ' + member.MemberName + ' reader')
##                filenameMember.AutoPipe = 0
                exec('self.'+filenameMember.MemberName+' = \'\'')
                self.InputMembers.append(filenameMember)

    def SetOutputMembers(self,membersToAppend):
        pypeMembersToAppend = self.ConvertToPypeMembers(membersToAppend)
        for member in pypeMembersToAppend:
            self.OutputMembers.append(member)
            if member.MemberIO:
                filenameMember = pypeMember(self.GetIOOutputFileNameMember(member.MemberName),self.GetIOFileNameOption(member.OptionName),'str',1,'filename for the default ' + member.MemberName + ' writer')
##                filenameMember.AutoPipe = 0
                exec('self.'+filenameMember.MemberName+' = \'\'')
                self.InputMembers.append(filenameMember)

    def SetScriptName(self,scriptName):
        self.ScriptName = scriptName

    def SetScriptDoc(self,scriptDoc):
        self.ScriptDoc = scriptDoc

    def GetUsageString(self):
        usageString = ''
        scriptUsageString = os.path.splitext(self.ScriptName)[0]
        if self.ScriptDoc != '':
            scriptUsageString += ' : ' + self.ScriptDoc
        useTextWrap = 1
        try:
            import textwrap
        except ImportError:
            useTextWrap = 0
        else:
            textwrapper = textwrap.TextWrapper()
            textwrapper.initial_indent = ''
            textwrapper.subsequent_indent = ' '
        if useTextWrap:
            usageString += textwrapper.fill(scriptUsageString)
        else:
            usageString += scriptUsageString
        for memberList in [self.InputMembers, self.OutputMembers]:
            if memberList == self.InputMembers :
                 usageString += '\n' + '  ' + 'Input arguments:'
            elif memberList == self.OutputMembers :
                 usageString += '\n' + '  ' + 'Output arguments:'
            for memberEntry in memberList:
                memberUsageString = ''
                indentation = '   '
                if useTextWrap:
                    textwrapper.initial_indent = indentation
                    textwrapper.subsequent_indent = indentation + '  '
                memberName  = memberEntry.MemberName
                option = memberEntry.OptionName
                memberType = memberEntry.MemberType
                memberLength = memberEntry.MemberLength
                memberDoc = memberEntry.MemberDoc
                if option!='':
                    default = 0
                    if memberLength == 0:
                        memberUsageString += '-' + option + ' ' + memberName
                    elif memberType in self.BuiltinOptionTypes:
                        default = self.__getattribute__(memberName)
                        memberUsageString += '-' + option + ' ' + memberName + '(' + memberType + ')'  + '[' + str(default) + ']'
                    else:
                        memberUsageString += '-' + option + ' ' + memberName + '(' + memberType + ')'
                    if memberDoc != '':
                        memberUsageString += ' : ' + memberDoc
                if useTextWrap:
                    usageString += '\n' + textwrapper.fill(memberUsageString)
                else:
                    usageString += '\n' + memberUsageString
        usageString += '\n'
        return usageString

    def GetDokuWikiUsageString(self):
        usageString = ''
        usageString = '======'
        usageString += self.ScriptName
        usageString += '======'
        usageString += '\n'
        if self.ScriptDoc != '':
            usageString += '=====Description=====' + '\n'
            usageString += self.ScriptDoc + '\n'
        for memberList in [self.InputMembers, self.OutputMembers]:
            if memberList == self.InputMembers :
                 usageString += '=====Input arguments=====' + '\n'
            elif memberList == self.OutputMembers :
                 usageString += '=====Output arguments=====' + '\n'
            usageString += '^ Argument ^ Variable ^ Type ^ Default ^ Description ^\n'
            for memberEntry in memberList:
                memberUsageString = ''
                memberName  = memberEntry.MemberName
                option = memberEntry.OptionName
                memberType = memberEntry.MemberType
                memberLength = memberEntry.MemberLength
                memberDoc = memberEntry.MemberDoc
                if option!='':
                    default = 0
                    if memberLength == 0:
                        memberUsageString += option + ' ' + memberName
                    elif memberType in self.BuiltinOptionTypes:
                        default = self.__getattribute__(memberName)
                        memberUsageString += '| ' + option + ' | ' + memberName + ' | ' + memberType + ' | '  + str(default) + ' | '
                    else:
                        memberUsageString += '| ' + option + ' | ' + memberName + ' | ' + memberType + ' | | '
                    if memberDoc != '':
                        memberUsageString += memberDoc
                    memberUsageString += ' | '
                memberUsageString += '\n'
                usageString += memberUsageString
        usageString += '\n'
        return usageString

    def ParseArguments(self):
        for arg in self.Arguments:
            if arg == '--help':
                self.PrintLog('')
                self.OutputText(self.GetUsageString())
                self.PrintLog('')
                return 0
            if arg == '--dokuwiki':
                self.PrintLog('')
                self.OutputText(self.GetDokuWikiUsageString())
                self.PrintLog('')
                return 0
            if (arg[0] == '-') & (len(arg)==1):
                self.PrintError(self.ScriptName + ' error: unknown option ' + arg + '\n' + self.GetUsageString())
                return 0
            if (arg[0] == '-'):
                if (arg[1] in string.ascii_letters):
                    matchingMembers = [member for member in self.InputMembers if member.OptionName in [arg.lstrip('-'), arg.lstrip('-').rstrip('@')]]
                    if not matchingMembers:
                        self.PrintError(self.ScriptName + ' error: unknown option ' + arg + '\n' + self.GetUsageString())
                        return 0

        for memberEntry in self.InputMembers:

            if not memberEntry.OptionName:
                continue

            memberName  = memberEntry.MemberName
            option = '-' + memberEntry.OptionName
            memberType = memberEntry.MemberType
            memberLength = memberEntry.MemberLength
            memberValues = []
            activated = 0
            explicitPipe = 0

            specifiedOptions = [arg for arg in self.Arguments if (arg[0] == '-') and (arg[1] in string.ascii_letters + '-')]
            
            pushedOption = option + '@'
            if pushedOption in specifiedOptions:
                memberEntry.Pushed = 1
                specifiedOptions[specifiedOptions.index(pushedOption)] = option
                self.Arguments[self.Arguments.index(pushedOption)] = option
            
            if option in specifiedOptions:
                if memberLength == 0:
                    activated = 1
                optionValues = []
                optionIndex = self.Arguments.index(option)
                if option != specifiedOptions[-1]:
                    nextOptionIndex = self.Arguments.index(specifiedOptions[specifiedOptions.index(option)+1])
                    optionValues = self.Arguments[optionIndex+1:nextOptionIndex]
                else:
                    optionValues = self.Arguments[optionIndex+1:]
                for value in optionValues:
                    if value[0] == '@':
                        memberEntry.ExplicitPipe = value[1:]
                    else: 
                        if memberType in self.BuiltinOptionTypes:
                            exec('castValue = '+memberType+'(\''+value+'\')')
                            memberValues.append(castValue)
                        else:
                            memberValues.append(value)
            else:
                continue

            if memberLength != -1:
                if (len(memberValues) != memberLength) and not memberEntry.ExplicitPipe:
                    self.PrintError('Error for option '+option+': '+str(len(memberValues))+' entries given, '+str(memberLength)+' expected.\n'+self.GetUsageString())
                    return 0

            if len(memberValues) > 0:
                if (memberLength==0):
                    if (activated == 1):
                        setattr(self,memberName,1)
                        memberEntry.MemberValue = 1
                elif (memberLength==1):
                    setattr(self,memberName,memberValues[0])
                    memberEntry.MemberValue = memberValues[0]
                else:
                    setattr(self,memberName,memberValues)
                    memberEntry.MemberValue = memberValues

            if (memberType != ''):
                if (memberLength==0):
                    if activated:
                        self.PrintLog(memberName + ' = ' + 'on',1)
                    else:
                        self.PrintLog(memberName + ' = ' + 'off',1)
                else:
                    if (memberLength==-1):
                        memberLength = len(memberValues)
                    if memberEntry.ExplicitPipe:
                        self.PrintLog(memberName+ ' = @' + memberEntry.ExplicitPipe,1)
                    else:
                        self.PrintLog(memberName+ ' = ' + str(self.__getattribute__(memberName)),1)
        return 1

    def IORead(self):
        for member in self.InputMembers:
            if member.MemberIO:
                exec('filename = self.' + self.GetIOInputFileNameMember(member.MemberName))
                if filename:
                    try:
                        exec('import ' + member.MemberIO)
                    except ImportError:
                        self.PrintError('Cannot import module ' + member.MemberIO + ' required for reading ' + member.MemberName)
                    exec('readerName = ' + member.MemberIO + '.' + member.MemberIO)
                    readerClassName = member.MemberIO + '.' + readerName
                    exec('reader = ' + readerClassName + '()')
                    reader.InputFileName = filename
                    reader.LogOn = self.LogOn
                    reader.InputStream = self.InputStream
                    reader.OutputStream = self.OutputStream
                    reader.Execute()
                    exec('self.' + member.MemberName + ' = reader.Output')

    def IOWrite(self):
        for member in self.OutputMembers:
            if member.MemberIO:
                exec('filename = self.' + self.GetIOOutputFileNameMember(member.MemberName))
                exec('input = self.' + member.MemberName)
                if filename:
                    try:
                        exec('import ' + member.MemberIO)
                    except ImportError:
                        self.PrintError('Cannot import module ' + member.MemberIO + ' required for writing ' + member.MemberIO)
                    exec('writerName = ' + member.MemberIO + '.' + member.MemberIO)
                    writerClassName = member.MemberIO + '.' + writerName
                    exec('writer = ' + writerClassName + '()')
                    writer.Input = input
                    writer.OutputFileName = filename
                    writer.LogOn = self.LogOn
                    writer.InputStream = self.InputStream
                    writer.OutputStream = self.OutputStream
                    writer.Execute()

    def GetIOInputFileNameMember(self,memberName):
        return memberName + 'InputFileName'

    def GetIOOutputFileNameMember(self,memberName):
        return memberName + 'OutputFileName'

    def GetIOFileNameOption(self,optionName):
        return optionName + 'file'

    def Execute(self):
        pass

    def Deallocate(self):
        pass

class pypeMain(object):

    def __init__(self):
        self.Arguments = None

    def Execute(self):
        import pype
        pipe = pype.Pype()
        pipe.Arguments = self.Arguments
        pipe.ParseArguments()
        pipe.Execute()

