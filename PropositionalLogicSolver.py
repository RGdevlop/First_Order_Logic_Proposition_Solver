def FindLeft(formula,i):
    x= i-1
    if(formula[i-1]==')'):
        count = 1
        for j in range(1, i):
            if (formula[i - j - 1] == '('):
                count -= 1
                if (count == 0):
                    x = i - j - 1
                    break;
            elif (formula[i - j - 1] == ')'):
                count += 1
    if(formula[x-1]=='!'):
        x-=1
    return x
def FindRight(formula,i):
    x=i+2
    if(formula[i+1]=='!'):
        x = i+3
    if(formula[i+1]=='('):
        count = 1
        for j in range (x,len(formula)):
            if(formula[j]==')'):
                count -= 1
                if(count == 0):
                    x = j+1
                    break;
            elif(formula[j]=='('):
                count +=1
    return x
def removeIff(formula):
    for j in range (0,len(formula)):
        for i in range (0,len(formula)):
            if(formula[i]!='='):
                continue
            else:
                x=FindLeft(formula,i)
                y=FindRight(formula,i)
               # print(x)
               # print(y)
                formula = formula [: x] + '(' + formula [x : i] + '>'+ formula [i+1:y] + ')&(' + formula[i+1:y] + '>' + formula[x:i] + ')' + formula[y :]
                if formula[-1] == ' ':
                    formula = formula[:len(formula)-1]
    return formula

def removeImpl(formula):
    i=0
    while(i<len(formula)):
        if(formula[i]!='>'):
            i+=1
            continue
        else:
            x = FindLeft(formula,i)
            if(formula[x]=='!'):
                formula = formula [: x] + formula[x+1:i] + '|' + formula[i+1:]
            else:
                formula = formula [: x] + '!' + formula [x : i] + '|' + formula[i+1 : ]
        i+=1
    return formula

def pushNot(formula):
    i=0
    while (i<len(formula)):
        if(formula[i]!='!'):
            i+=1
            continue
        elif(formula[i+1]!='('):
            i+=1
            continue
        else:
            formula = formula[ : i] + formula[i+1:]
            j= i+1
            while(j<len(formula)):
                if(formula[j]==')'):
                    j+=1
                    break
                if(formula[j]=='('):
                    count=1
                    init = j
                    j+=1
                    while(count):
                        if(formula[j]=='('):
                            count+=1
                        elif(formula[j]==')'):
                            count-=1
                        j+=1
                    formula = formula[: init] + '!' + formula [init:]
                elif(formula[j]=='!'):
                    formula = formula[ : j] + formula[j+1:]
                elif(formula[j]=='&'):
                    formula = formula [: j] + '|' + formula[j+1 :]
                elif(formula[j]=='|'):
                    formula = formula [: j] + '&' + formula[j+1 :]
                else:
                    formula = formula [: j] + '!' + formula[j : ]
                    j+=1
                j+=1
        i+=1
    return formula

def distributeOr(formula, pos):
    right = FindRight(formula,pos)
    left = FindLeft(formula,pos)
    #print(formula)
    #print(pos)
    #print(right)
    #print(left)
    if(formula[pos-1]==')' and formula[pos+1]!='('):
        sub = formula [left+1: pos-1]
        #print(sub)
        if(sub[0]=='(' or sub[len(sub)-1]==')'):
            z = ''
            j = 0
            if(sub[0]=='('):
                count = 1
                j=1
                while(j<len(sub)):
                    if(sub[j]==')'):
                        count-=1
                        if(count==0):
                            break
                    elif(sub[j]=='('):
                        count+=1
                    j+=1
                if(sub[j+1]=='|'):
                    z  = distributeOr(sub,j+1)
                    return formula[: left] + z + formula[pos:]
            elif(sub[len(sub)-1]==')'):
                k = len(sub)-2
                count = 1
                while(k>0):
                    if(sub[k]==')'):
                        count+=1
                    elif(sub[k]=='('):
                        count-=1
                        if(count==0):
                            break
                    k+=1
                if(sub[k-1]=='|'):
                    z = distributeOr(sub, k-1)
                    return formula[: left] + z + formula[pos:]
                elif(sub[k-1]=='&'):
                    d1 = sub[ : k-1]
                    d2 = sub[k:]
                    r1 = formula[pos+1:right]
                    afterDis = '(' + d1 + '|' + r1 + ')&(' + d2 + '|' + r1 + ')'
                    formula = formula[0:left] + afterDis + formula[right:]
                    return formula
        else:
            d1 = ''
            d2 = ''
            op = ''
            if(sub[0]=='!'):
                d1='!' + sub[1]
                op = sub[2]
                if(sub[3]=='!'):
                   d2 = '!' + sub[4]
                else:
                    d2 = sub[3]
            else:
                d1 = sub[0]
                op = sub[1]
                if(sub[2]=='!'):
                    d2 = '!' + sub[3]
                else:
                    d2 = sub[2]
            r1 = formula[pos+1: right]
            if(op == '|'):
                #print(r1)
                afterDis = sub +  '|' + r1
            elif(op == '&'):
                afterDis = '(' + d1 + '|' + r1 + ')' + op + '(' + d2 + '|' + r1 + ')'
            formula = formula [0:left] + afterDis + formula [right : ]
            return formula
    elif (formula[pos - 1] != ')' and formula[pos + 1] == '('):
        sub = formula[pos + 2: right-1]
        if (sub[0] == '(' or sub[len(sub) - 1] == ')'):
            z = ''
            j = 0
            if (sub[0] == '('):
                count = 1
                j = 1
                while (j < len(sub)):
                    if (sub[j] == ')'):
                        count -= 1
                        if (count == 0):
                            break
                    elif (sub[j] == '('):
                        count += 1
                    j += 1
                #print(j)
                #print(sub)
                if (sub[j + 1] == '|'):
                    z = distributeOr(sub, j + 1)
                    return formula[0:pos+1] + z + formula [right:]
                elif (sub[j + 1] == '&'):
                    #print(formula)
                    d1 = sub[: j+1]
                    d2 = sub[j+2:]
                    r1 = formula[left:pos]
                    afterDis = '(' + r1 + '|' + d1 + ')&(' + r1 + '|' + d2 + ')'
                    #print(afterDis)
                    formula = formula[0:left] + afterDis + formula[right:]
                    return formula
            elif (sub[len(sub) - 1] == ')'):
                k = len(sub) - 2
                count = 1
                while (k > 0):
                    if (sub[k] == ')'):
                        count += 1
                    elif (sub[k] == '('):
                        count -= 1
                        if (count == 0):
                            break
                    k -= 1
                if (sub[k - 1] == '|'):
                    z = distributeOr(sub, k - 1)
                elif (sub[k - 1] == '&'):
                    #print("here")
                    #print(sub)
                    d1 = sub[: k-1]
                    d2 = sub[k:]
                    r1 = formula[left:pos]
                    afterDis = '(' + r1 + '|' + d1 + ')&(' + r1 + '|' + d2 + ')'
                    #print(afterDis)
                    formula = formula[0:left] + afterDis + formula[right:]
                    return formula
            formula =  formula[: pos+2] + z + formula[right-1:]
            return formula
        else:
            d1 = ''
            d2 = ''
            op = ''
            if (sub[0] == '!'):
                d1 = '!' + sub[1]
                op = sub[2]
                if (sub[3] == '!'):
                    d2 = '!' + sub[4]
                else:
                    d2 = sub[3]
            else:
                d1 = sub[0]
                op = sub[1]
                if (sub[2] == '!'):
                    d2 = '!' + sub[3]
                else:
                    d2 = sub[2]
            r1 = formula[left : pos]
            if (op == '|'):
                afterDis = r1 + '|' + sub
            elif (op == '&'):
                afterDis = '(' + r1 + '|' + d1 + ')' + op + '(' + r1 + '|' + d2 + ')'
            formula = formula[0:left] + afterDis + formula[right:]
        return formula
    if(formula[pos-1]==')' and formula[pos+1]=='('):
        sub1 = formula [left+1: pos-1]
        sub2 = formula [pos+2 : right-1]
        if(sub1[0]=='(' or sub1[len(sub1)-1]==')'):
            sub = sub1
            z = ''
            j = 0
            if (sub[0] == '('):
                count = 1
                j = 1
                while (j < len(sub)):
                    if (sub[j] == ')'):
                        count -= 1
                        if (count == 0):
                            break
                    elif (sub[j] == '('):
                        count += 1
                    j += 1
                if (sub[j + 1] == '|'):
                    z = distributeOr(sub, j + 1)
            elif (sub[len(sub) - 1] == ')'):
                k = len(sub) - 2
                count = 1
                while (k > 0):
                    if (sub[k] == ')'):
                        count += 1
                    elif (sub[k] == '('):
                        count -= 1
                        if (count == 0):
                            break
                    k += 1
                if (sub[k - 1] == '|'):
                    z = distributeOr(sub, k - 1)
                    return formula[: left] + z + formula[pos:]
                elif (sub[k - 1] == '&'):
                    d1 = sub[: k - 1]
                    d2 = sub[k:]
                    r1 = formula[pos + 1:right]
                    afterDis = '(' + d1 + '|' + r1 + ')&(' + d2 + '|' + r1 + ')'
                    formula = formula[0:left] + afterDis + formula[right:]
                    return formula
        if (sub2[0] == '(' or sub2[len(sub2)-1] == ')'):
            sub = sub2
            z = ''
            j = 0
            if (sub[0] == '('):
                count = 1
                j = 1
                while (j < len(sub)):
                    if (sub[j] == ')'):
                        count -= 1
                        if (count == 0):
                            break
                    elif (sub[j] == '('):
                        count += 1
                    j += 1
                if (sub[j + 1] == '|'):
                    z = distributeOr(sub, j + 1)
            elif (sub[len(sub) - 1] == ')'):
                k = len(sub) - 2
                count = 1
                while (k > 0):
                    if (sub[k] == ')'):
                        count += 1
                    elif (sub[k] == '('):
                        count -= 1
                        if (count == 0):
                            break
                    k += 1
                if (sub[k - 1] == '|'):
                    z = distributeOr(sub, k - 1)
                    return formula[: left] + z + formula[pos:]
                elif (sub[k - 1] == '&'):
                    d1 = sub[: k - 1]
                    d2 = sub[k:]
                    r1 = formula[pos + 1:right]
                    afterDis = '(' + d1 + '|' + r1 + ')&(' + d2 + '|' + r1 + ')'
                    formula = formula[0:left] + afterDis + formula[right:]
                    return formula
        else:
            d1 = ''
            d2 = ''
            op = ''
            if (sub1[0] == '!'):
                d1 = '!' + sub1[1]
                op = sub1[2]
                if (sub1[3] == '!'):
                    d2 = '!' + sub1[4]
                else:
                    d2 = sub1[3]
            else:
                d1 = sub1[0]
                op = sub1[1]
                if (sub1[2] == '!'):
                    d2 = '!' + sub1[3]
                else:
                    d2 = sub1[2]
            r1 = '(' + sub2 + ')'
            if (op == '|'):
                if (sub2[0] == '!'):
                    d3 = '!' + sub1[1]
                    op1 = sub2[2]
                    if (sub2[3] == '!'):
                        d4 = '!' + sub2[4]
                    else:
                        d4 = sub2[3]
                else:
                    d3 = sub2[0]
                    op1 = sub2[1]
                    if (sub2[2] == '!'):
                        d4 = '!' + sub2[3]
                    else:
                        d4 = sub2[2]
                if(op1=='|'):
                    afterDis = sub1 + '|' + r1
                    formula = formula[0:left] + afterDis + formula[right:]
                elif(op1=='&'):
                    r1 = '(' + sub1 + ')'
                    afterDis = '(' + r1 + '|' + d3 + ')' +op1 + '(' + r1 + "|" + d4 + ')'
                    formula = formula[0:left] + afterDis + formula[right:]
            elif (op == '&'):
                afterDis = '(' + d1 + '|' + r1 + ')' + op + '(' + d2 + '|' + r1 + ')'
                formula = formula[0:left] + afterDis + formula[right:]
        return formula



def Refactor(formulaList,length):
    n= int(length)
    i=0
    while(i<n):
        formula = formulaList[i]
       # print(formula)
        if( not (formula[0]=='(' or formula[len(formula)-1]==')' )):
            i+=1
            continue
        else:
            j=0
            first=0
            x=0
            count=0
            while(j<len(formula)):
                if(formula[j]!='(' and formula[j]!=')'):
                    j+=1
                    continue
                elif(formula[j]=='('):
                    if(count==0):
                        first=j
                    count+=1
                elif(formula[j]==')'):
                    count-=1
                    if(count==0):
                        x=j
                        break
                j+=1
            if(first==0):
                if(x+1 == len(formula)):
                    formula = formula[1:len(formula)-1]
                    formulaList[i] = '#'
                    formulaList.append(formula)
                    n+=1
                    i+=1
                    continue
                if(formula[x+1]=='|'):
                    #print(formula)
                    formula = distributeOr(formula,x+1)
                    formulaList.append(formula)
                    formulaList[i]='#'
                    n+=1
                elif(formula[x+1]=='&'):
                    a = formula[1:x]
                    b= formula [x+2 : len(formula)]
                    formulaList.append(a)
                    formulaList.append(b)
                    formulaList[i]='#'
                    n+=2
            else:
                if(formula[first-1]=='|'):
                    #print(formula)
                    formula = distributeOr(formula,first-1)
                    formulaList.append(formula)
                    formulaList[i]='#'
                    n+=1
                elif(formula[first-1]=='&'):
                    a= formula[ : first-2]
                    b = formula [first+1 : len(formula) -1 ]
                    formulaList.append(a)
                    formulaList.append(b)
                    formulaList[i]='#'
                    n+=2
        i+=1
    List = []
    for formula in formulaList:
        if formula != "#":
            List.append(formula)
    #print(List)
    return List
def ReFormat(formula):
    x = formula
    list = x.split('|')
    form = ''
    cont = set()
    for n in list:
        if negation(n) in list or n in cont:
            continue
        cont.add(n)
        if(form == ''):
            form = n
        else:
            form += '|' + n
    return form
def ToCNF(formulaList, n):
    for i in range (0,int(n)):
        formula = formulaList[i]
        formula = removeIff(formula)
        formula = removeImpl(formula)
        formula = pushNot(formula)
        formulaList[i] = formula
    formList = []
    for formula in formulaList:
        List = []
        List.append(formula)
        List = Refactor(List,1)
        for form in List:
            form = ReFormat(form)
            if form=='' :
                #formList.append(form)
                continue
            if len(form) >2 and form[0]!='!' and form[1]=='&' and len(form)<5:
                formList.append(form[0])
                formList.append(form[2:])
            elif len(form) >2 and form[-2] =='&' and len(form)<5:
                formList.append(form[-1])
                formList.append(form[:-2])
            elif len(form)==5 and form[0]=='!' and form[-2]=='!' and form[-3] =='&':
                formList.append(form[0:2])
                formList.append(form[3:])
            else:
                formList.append(form)
    #print(formList)
    return formList

def isNegation(form, formula):
    if len(form) > 2 or len(formula) > 2:
        return False
    if form[0] == '!' and form[1:] == formula:
        return True
    if formula[0] == '!' and formula[1:] == form:
        return True
    return False
def negation(formula):
    if formula[0] == '!':
        return formula[1:]
    else:
        return '!' + formula
def prove(formulaList , m , toProve):
    l = formulaList
    for formula in formulaList:
        #print("current:"+formula)
        if formula == '#':
            continue
        for form in formulaList:
            #if formula == '!R':
                #print(form)
            if form == formula or form == '#' or formula == '#' :
                continue
            if isNegation(form,formula):
                if(m == '1'):
                    print("Empty Clause(using " + form +" and " +formula+')')
                return 1
            j = formula
            List = j.split('|')
            for entry in List:
                if form == '#':
                    break
                k = form
                s = k.split('|')
                if negation(entry) in s:
                    place1 = form.find(negation(entry))
                    place2 = formula.find(entry)
                    x = form[:place1 -1 ] + '|' + form[place1 + len(negation(entry)) + 1 :]
                    y = formula[:place2 -1] + '|' + formula[place2 + len(entry) +1 :]
                    if place1 == 0:
                        x = form[place1 + len(negation(entry)) +1 :]
                    elif place1 == len(form) - 1  or place1 == len(form) - 2:
                        #print(place1)
                        #print(form)
                        x = form[:place1-1]
                    if place2 == 0:
                        y = formula[place2 + len(entry) +1 :]
                    elif place2 + len(entry) == len(formula):
                        y = formula[:place2 -1]
                    append = x + '|' + y
                    if x == '':
                        append = y
                    if y == '':
                        append  = x
                    if x == y:
                        append = x
                    #print(append)
                    #print(formula)
                    append = ReFormat(append)
                    if(append == ''):
                        continue
                    if(m == '1'):
                        print(append + '(using ' + form + ' and ' + formula + ')')
                    if(append == toProve):
                        if (m == '1'):
                            print('Empty Clause(Using ' + append + ' and ' + negation(toProve)+ ')')
                        return 1
                    if(append == negation(toProve)):
                        if (m == '1'):
                            print('True Clause(Using' + form + ' and ' + formula + ')')
                        return 0
                    #formulaList[formulaList.index(form)] = '#'
                    #formulaList[formulaList.index(formula)] = '#'
                    formulaList.append(append)
                    form = '#'
                    formula = '#'
                    continue
    #x = l[-1]
    #l[-1] = l[0]
    #l[0] = x
    #prove(l , m , toProve)
    return 0
n,m = input().split()
formulaList = []
for i in range (0,int(n)):
    formula = input()
    formulaList.append(formula)
toProve = input()
if len(toProve) == 1:
    formulaList.append('!' + toProve)
elif len(toProve) == 2:
    formulaList.append(toProve[1])
else:
    toProve = removeIff(toProve)
    toProve = removeImpl(toProve)
    formulaList.append(pushNot('!(' +toProve+')') )
formulaList = ToCNF(formulaList,n)
if m == '1':
    for formula in formulaList:
        print(formula)
result = prove(formulaList, m ,toProve)
print(result)