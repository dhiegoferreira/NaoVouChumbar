import string
import openpyxl
from datetime import datetime, timedelta


MondayColumnValueExcel = 2 # BC columns merged
TuesdayColumnValueExcel = 4 # DE columns merged
WednesdayColumnValueExcel = 6 # FG  columns merged
ThurdayColumnValueExcel = 8 # HI  columns merged
FridayColumnValueExcel = 10 # JK  columns merged
SaturdayColumnValueExcel = 12 # LM  columns merged

StartIndex1St = 11

studentYears = [ "1º ano","2º ano","3º ano"]

DaysColumnInExcel = [2,4,6,8,10,12]

def parse_cell(cell_value):
    events = []
    for line in cell_value.split('\n'):
        if line.strip():
            time, *description = line.split(' ', 1)
            events.append({
                'time': time,
                'description': description[0] if description else ''
            })
    return events

def parse_schedul_1St(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    schedule = []


    for row in range(StartIndex1St, sheet.max_row + 1):
        week = sheet.cell(row, column=1).value #week number match with gisem
        
        if week and isinstance(week, int): #is a valid integer? I know that will start a new valid week
            studentYearPrevious = ""
            indexStartDate = row+1 #always week number row + 1 that is the row that contains date
            for weekRowFrame in range(indexStartDate,indexStartDate+12):
                
                nextWeekRow = sheet.cell(weekRowFrame+1, column=1).value #week number match with gisem
                if nextWeekRow and isinstance(nextWeekRow, int):
                    break
                
        
                for day in DaysColumnInExcel:  # Monday to Saturday
                    indexStartDataFromYearStudent = weekRowFrame+1
                    
                    dateWeekFrame = str(sheet.cell(indexStartDate,column=day).value)
                    splittedValue = dateWeekFrame.split("-")
                    
                    dayDate = int(splittedValue[2].split(' ')[0])
                    monthDate = int(splittedValue[1])
                    yearDate = int(splittedValue[0])
                
                    dateFormmated = datetime.strptime(f"{dayDate}/{monthDate}/{yearDate}", "%d/%m/%Y")
      
                    #migth be data from the date of each day in the week
                    ## in each row can contain for col=1 the student year
                    ## and 1 or util 4 event for each student year
                    ##Get Year data
                    studentYear = str(sheet.cell(indexStartDataFromYearStudent,1).value)
                    mightBeEvent = str(sheet.cell(indexStartDataFromYearStudent, column=day).value)
                    
                    if(studentYear in studentYears):
                        #add new event for in a row that contains the year student field
                        if str.isalpha(mightBeEvent) and mightBeEvent != "" and mightBeEvent != "None":
                            events = parse_cell(mightBeEvent)
                            for event in events:
                                schedule.append({
                                    'date': dateFormmated,
                                    'studentYear': studentYear,
                                    'time': event['time'],
                                    'description': event['description']
                                })
                        
                        studentYearPrevious = studentYear
                    else:
                        #just add events for this existing year
                        #add new event for in a row that contains the year student field
                        if mightBeEvent != "" and mightBeEvent != "None":
                            events = parse_cell(mightBeEvent)
                            for event in events:
                                schedule.append({
                                    'date': dateFormmated,
                                    'studentYear': studentYearPrevious,
                                    'time': event['time'],
                                    'description': event['description']
                                })

                                       
    return schedule

def main():
    file_path = 'data.xlsx'
    schedule = parse_schedul_1St(file_path)
    
    for event in schedule:
        print(f"Date: {event['date'].strftime('%Y-%m-%d')}, "
              f"Year: {event['studentYear']}, "
              f"Time: {event['time']}, "
              f"Description: {event['description']}")

if __name__ == "__main__":
    main()