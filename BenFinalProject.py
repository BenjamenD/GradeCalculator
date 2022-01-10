import tkinter.filedialog as tk
import csv
import os
#imports for creating file search windows, manipulating csv files and os commands

def fileInfo(): # gather data from files and save in lists
    global d, TAinfo, Profinfo
    d = dict([])
    TAinfo = []
    Profinfo = []

    print("Follow instructions at the top left of the explorer windows, or in this window.")
    root = tk.Tk()
    root.withdraw()

    try:
        print("Find and open the professor csv file")
        prof = tk.askopenfilename(title = "Select the professors file")
        ProfFile = open(prof, "r")
        csvProf = csv.reader(ProfFile)
        for row in csvProf:
            Profinfo.append(row)

    except: 
        print("Professor file not accesible.")
        os.system("pause")
        exit()
        
    try:
        print("Find and open the TA csv file")
        TA = tk.askopenfilename(title = "Select the TA file")
        TAfile = open(TA, "r")
        csvTA= csv.reader(TAfile)
        for row in csvTA:
            TAinfo.append(row)

    except: # stop program if either filename is typed incorrectly
        print("TA file not accessable.")
        os.system("pause")
        exit()

    ProfFile.close()
    TAfile.close()
    

def quizGrades(): # assign quiz and exam grades to dictionary
    for row in Profinfo[1:]:
        q1 = eval(row[1])/25
        q2 = eval(row[2])/20
        q3 = eval(row[3])/25
        q4 = eval(row[4])/10
        q5 = eval(row[5])/10
        q = q1 + q2 + q3 + q4 + q5
        
        d[row[0]].append(q*5)
        d[row[0]].append(eval(row[6])/100*30)


def assignmentGrades(): # assign midterm and assignment grades to dictionary
    for i in TAinfo[1:]:
        allGrades = 0
        for grade in i[2:12]:
            allGrades = allGrades + eval(grade)
        d[i[0]].append((allGrades/10)*2)
        d[i[0]].append(eval(i[12]))

        
def attendance(): # assign pass/fail to dictionary according to attendance
    start = TAinfo[0].index("Attendance")
    for row in TAinfo[1:]:
        insufficient = False
        totalA = 0
        consecA = 0
        totalP = 0
        for i in row[start]:
            if i == "A":
                consecA = consecA + 1
                totalA = totalA + 1
            else:
                totalP = totalP + 1
                if consecA == 3:
                    insufficient = True
                consecA = 0
        if insufficient or consecA == 3 or totalA >= 5:
            d[row[0]]= ["Fail"]
        else:
            d[row[0]]= ["Pass"]

        d[row[0]].append(totalP)


def finalGrades(): # assigning final grade to dictionary
    for student in d:
        totalGrade = 0
        for grade in d[student][1:]:
            totalGrade = totalGrade + grade
        d[student].append(totalGrade)


def topScore(): # assigns all students who share highest grade to a list
    students = []
    top = 0
    for i in d:
        if d[i][6] > top:
            top = d[i][6]
            students = [i]
        elif d[i][6] == top:
            students.append(i)
    return students, top


def mean(): # calculates mean grade 
    amtGrades = 0
    allGrades = 0
    for i in d:
        if d[i][0] != "Fail":
            amtGrades = amtGrades + 1
            allGrades = allGrades + d[i][6]
    mean = allGrades/amtGrades
    return mean


def median(): # calculates median grade
    passingS = []
    for i in d:
        if d[i][0] == "Pass":
            passingS.append(d[i][6])
    passingS.sort()
    if len(passingS)%2 != 0:
        med = passingS[int(len(passingS)/2)]
    else:
        med = passingS[int(len(passingS)/2)], passingS[int(len(passingS)/2)-1]
    return med

    
def finalFile(): # creates a new file to hold all names and grades
    print("Go to the location you would like to save the final grades file, type in the name and extension and save")
    final = tk.asksaveasfilename(title="Select the name, location and extension you would like to give the final grades file")
    Grades = open(final,"w", newline='')
    final = csv.writer(Grades)
    final.writerow(["Full Name","Final grades (rounded to hundredth digit)"])
    for i in d:
        final.writerow([i,round(d[i][6],2)])
    Grades.close()
   
        
def passingFile(): # creates a new file to hold initials and grades of passing students
    print("Go to the location you would like to save the passing students file, type in the name and extension and save")
    passed = tk.asksaveasfilename(title="Select the name and location you would like to give the passed students file")
    passingGrades = open(passed,"w", newline='')
    wrtPass = csv.writer(passingGrades)
    wrtPass.writerow(["Initals", "Final grades (rounded to hundredth digit)"])
    for i in d:
        if d[i][0] == "Pass" and d[i][6] >= 50:
            last = i.split(" ")[1][0].upper()
            first = i.split(" ")[0][0].lower()
            wrtPass.writerow([first+ last,round(d[i][6],2)])
    passingGrades.close()
    
        
def statsFile(): # creates file containing students with highest grades, median and mean grades
    print("Go to the location you would like to save the stats file, type in the name and extension and save")
    stats = tk.asksaveasfilename(title="Select the name and location you would like to give the stats file")
    statisticsFile = open(stats,"w", newline='')
    wrtStat = csv.writer(statisticsFile)
    wrtStat.writerows([["The following data hasn't been rounded"],["Highest scoring student: ", topScore()[0]],["Highest grade: ", topScore()[1]],["Median class grade: ", median()],["Mean class grade: ", mean()]])
    statisticsFile.close()


def failedFile(): # creates file containting inintials of failed students
    print("Go to the location you would like to save the failed students file, type in the name and extension and save")
    failed = tk.asksaveasfilename(title="Select the name and location you would like to give the failed students file")
    failFile = open(failed,"w", newline='')
    wrtFail = csv.writer(failFile)
    wrtFail.writerow(["Initals"])
    for i in d:
        if d[i][0] == "Fail" or d[i][6] <= 50:
            last = i.split(" ")[1][0].upper()
            first = i.split(" ")[0][0].lower()
            wrtFail.writerow([first+ last])
    failFile.close()


def main():    
    fileInfo()
    attendance()
    quizGrades()
    assignmentGrades()
    finalGrades()
    finalFile()
    passingFile()
    statsFile()
    failedFile()
    print("Files have been created in specified directories.")
    os.system("pause")
    
main()
