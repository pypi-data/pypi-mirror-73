import ThamizhiLP
import re
import os
import subprocess

def analyseV(x) :
        x=ThamizhiLP.TamilNormalizer(x)
        x=ThamizhiLP.SandhiRemover(x)
        result="found"
        if(ThamizhiLP.ValidateTamilWord(x)==1) :
                for cno in ['verbs3','verbs4','verbs62','verbs11','verbs12','verbs-rest','verb-guesser']:
                        model=cno+".fst"
                        command="echo "+x+" | flookup "+model
                        output=os.popen(command).read()
                        output=str(output).strip()
                        findstr="verb"
                        if findstr in output:
                               result= output
                               break
                        else:
                               result="not found"
        return result

def analyseN(x) :
        x=ThamizhiLP.TamilNormalizer(x)
        x=ThamizhiLP.SandhiRemover(x)
        result="found"
        if(ThamizhiLP.ValidateTamilWord(x)==1) :
                for cno in ['noun']:
                        model=cno+".fst"
                        command="echo "+x+" | flookup "+model
                        output=os.popen(command).read()
                        output=str(output).strip()
                        findstr="noun"
                        if findstr in output:
                               result= output
                               break
                        else:
                               result="not found"
        return result

def analyseGuesserN(x) :
        x=ThamizhiLP.TamilNormalizer(x)
        x=ThamizhiLP.SandhiRemover(x)
        result="found"
        if(ThamizhiLP.ValidateTamilWord(x)==1) :
                for cno in ['noun-guesser']:
                        model=cno+".fst"
                        command="echo "+x+" | flookup "+model
                        output=os.popen(command).read()
                        output=str(output).strip()
                        findstr="noun"
                        if findstr in output:
                               result= output
                               break
                        else:
                               result="not found"
        return result

def analyseGuesserV(x) :
        x=ThamizhiLP.TamilNormalizer(x)
        x=ThamizhiLP.SandhiRemover(x)
        result="found"
        if(ThamizhiLP.ValidateTamilWord(x)==1) :
                for cno in ['verb-guesser']:
                        model=cno+".fst"
                        command="echo "+x+" | flookup "+model
                        output=os.popen(command).read()
                        output=str(output).strip()
                        findstr="noun"
                        if findstr in output:
                               result= output
                               break
                        else:
                               result="not found"
        return result
                        
def analyse(word) :
        finalresults=""
        if "not" not in analyseV(word.strip()):
                finalresults=finalresults+"Verb: "+analyseV(word.strip())+"\n"
        if "not" not in analyseN(word.strip()):
                finalresults=finalresults+"Noun: "+analyseN(word.strip())+"\n"
        if "not" not in analyseN(word.strip()):
                finalresults=finalresults+"Noun Guesser: "+analyseGuesserN(word.strip())+"\n"
        if "not" not in analyseN(word.strip()):
                finalresults=finalresults+"Verb Guesser: "+analyseGuesserV(word.strip())+"\n"

        return finalresults
analysis=analyse("கடலை");
print(analysis)
