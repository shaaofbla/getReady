from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Set up the WebDriver (e.g., using Chrome)
driver = webdriver.Firefox()

driver.implicitly_wait(2)


def compileIdFromString(text):
    text = text.replace("(","")
    text = text.replace(")","")
    words = text.split(" ")
    id = str()
    for word in words:
        id = id + word[0]
        
    if id == 'GZ':
        id = words[0][0:2]+words[1][0]

    return id

def parseMathTargets():
    letters = {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E"
        }
    try:
        driver.get('https://app-p-kompetenzraster.azurewebsites.net/#/professionspublic/0ea79c50-f9dc-4760-b725-b357135d3db6')
        content = driver.find_elements("class name","theme-container")

        for container in content:
            thema = container.find_element("class name", "theme-name")
            label_level0 = thema.text
            id_level0 = compileIdFromString(label_level0)
            print(id_level0)
            subTables = container.find_elements("tag name", "table")
            #html = thema.get_attribute('innerHTML')
            #print(html)
            #subTables = thema.find_elements("class name", "competenceTable")
            
            for table in subTables:                
                area = table.find_element("class name", "areaTitle")
                label_level1 = area.find_element("tag name", "td").text
                print("\t"+label_level1)
                id_level1 = compileIdFromString(label_level1)
                id_level1_con = id_level0 + id_level1
                print("\t"+id_level0+id_level1)
                rows = table.find_elements("tag name", "tr")
                rows.pop(0) # get rid of first element, its the area Title
                """
                ## Get row Names
                for row in rows:
                    rowName = row.find_element("tag name", "td")
                    #print(rowName.get_attribute('innerHTML'))
                    rowName = rowName.find_elements("tag name", "span")
                    id_level2 = rowName[0].text
                    id_level2_con = id_level1_con + id_level2
                    label_level2 = rowName[1].text
                    print("\t\t"+id_level2_con)
                    print("\t\t"+label_level2)
                
                ## Get Row Elements
                for row in rows:
                    elements = row.find_elements("tag name", "td")
                    elements.pop(0) #Get rid of row name
                    print(len(elements))
                    for i, element in enumerate(elements):
                        try:
                            label_level3 = element.find_element("class name", "ng-binding")
                            id_level3 = letters[i]
                            id_level3_con = id_level2_con+id_level3
                            print("\t\t\t"+id_level3_con+" "+label_level3.text)
                        except NoSuchElementException:
                            print("No Element found..")                            
                """
                print(len(rows))

    finally:
        print("closing...")
        driver.close()

parseMathTargets()

def goThruJoblist():
# Load the page
    jobs = []
    try:
        driver.get('https://app-p-kompetenzraster.azurewebsites.net/#/')
        content = driver.find_elements("tag name","td")

        for row in content:
            job = row.find_element("tag name", "a").text
            print(job)
            jobs.append(job)
        content[0].find_element("tag name","a").click()

    finally:
        print("closing...")
        driver.close()

#print(len(jobs))
# Locate the table (using an appropriate selector)
#table = driver.find_element_by_css_selector('table.competenceTable')

# Locate the elements where the background color is applied
#cells = table.find_elements_by_css_selector('div.competence-item-background')

# Extract and print the background color
"""
for cell in cells:
    color = cell.value_of_css_property('background-color')
    print(color)

"""
# Close the browser
driver.quit()