from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up the WebDriver (e.g., using Chrome)
driver = webdriver.Firefox()

driver.implicitly_wait(2)


def compileIdFromString(Str):
    words = Str.split(" ")
    id = str()
    for word in words:
        id = id + word[0]
    return id

def parseMathTargets():
    try:
        driver.get('https://app-p-kompetenzraster.azurewebsites.net/#/professionspublic/0ea79c50-f9dc-4760-b725-b357135d3db6')
        content = driver.find_elements("class name","theme-container")

        for container in content:
            thema = container.find_element("class name", "theme-name")
            themaName = thema.text
            print(themaName)
            id_level1 = compileIdFromString(themaName)
            print(id_level1)
            subTables = container.find_elements("tag name", "table")
            #html = thema.get_attribute('innerHTML')
            #print(html)
            #subTables = thema.find_elements("class name", "competenceTable")
            
            for table in subTables:                
                area = table.find_element("class name", "areaTitle")
                areaText = area.find_element("tag name", "td").text
                print("\t"+areaText)
                id_level2 = compileIdFromString(areaText)
                print("\t"+id_level1+id_level2)
                rows = table.find_elements("tag name", "tr")
                rows = rows[1:-1] # get rid of first element, its the area Title
                for row in rows:
                    columns = row.find_element("tag name", "td")
                    print(columns.get_attribute('innerHTML'))
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