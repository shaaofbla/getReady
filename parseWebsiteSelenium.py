from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import json
import time

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

def parseMathTargetsLabels():
    idsToLabels = {}
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
            if (id_level0 not in idsToLabels):
                idsToLabels[id_level0] = label_level0
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
                if (id_level1_con not in idsToLabels):
                    idsToLabels[id_level1_con] = label_level1
                rows = table.find_elements("tag name", "tr")
                rows.pop(0) # get rid of first element, its the area Title
                
                ## Get Row Elements
                for row in rows:
                    elements = row.find_elements("tag name", "td")
                    rowName = elements[0]
                    rowName = rowName.find_elements("tag name", "span")
                    id_level2 = rowName[0].text
                    id_level2_con = id_level1_con + id_level2
                    label_level2 = rowName[1].text
                    if (id_level2_con not in idsToLabels):
                        idsToLabels[id_level2_con] = label_level2
                    print("\t\t"+id_level2_con)
                    print("\t\t"+label_level2)

                    elements.pop(0) #Get rid of row name
                    print(len(elements))
                    for i, element in enumerate(elements):
                        try:
                            subCells = element.find_elements("class name", "ng-binding")
                            for j, cell in enumerate(subCells):
                                label_level3 = cell.text
                                id_level3 = letters[i]+str(j+1)
                                id_level3_con = id_level2_con+id_level3
                                print("\t\t\t"+id_level3_con+" "+label_level3)
                                if (id_level3_con not in idsToLabels):
                                    idsToLabels[id_level3_con] = label_level3
                        except NoSuchElementException:
                            print("No Element found..")                            
                
                print(len(rows))
        print(idsToLabels)
        with open("MathTargetsIdsToLabels.json", "w") as outfile:
            json.dump(idsToLabels, outfile, indent=4)
        outfile.close()

    finally:
        print("pars Math Labels closing...")
        driver.close()

def clickMinus(driver):
    minus = driver.find_element("class name", "icon-minus-2")
    minus.click()
    driver.implicitly_wait(5)

def parseGermanTargetsLabels(url):
    idsToLabels = {}
    germanTargets = {}
    letters = {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E"
        }
    fields = {
        0: "Hören",
        1: "Sprechen",
        2: "Lesen",
        3: "Schreiben",
        }
    

    try:
        #driver.get('https://app-p-kompetenzraster.azurewebsites.net/#/professionspublic/0ea79c50-f9dc-4760-b725-b357135d3db6')
        driverGerman = webdriver.Firefox()
        driverGerman.implicitly_wait(2)

        driverGerman.get(url)
        container = driverGerman.find_element("class name", "button-container")
        buttons = container.find_elements("class name","grid-selection-btn")
        buttons[1].click()

        driverGerman.implicitly_wait(2)
   
        #plus = driver.find_elements("class name", "icon-plus-2")
        #arrow = driver.find_elements("class name", "arrow-header-container")
        content = driverGerman.find_elements("class name","theme-container")

        #tables = content[0].find_elements("class name", "table")
        for s,container in enumerate(content):
            tables = container.find_elements("class name", "table")
            # Hören
            germanTargets[fields[s]] = {}
            
            for t,table in enumerate(tables):
                print(f't: {t}')
                #print(table.get_attribute("innerHTML"))
                rows = table.find_elements("tag name", "tr")

                cell = rows[0].find_element("tag name", "td")
                label = cell.get_attribute("innerHTML")
                label=label.split()
                label = " ".join(label)
                
                print(f'label: {label}')

                cell = rows[1].find_elements("tag name", "td")
                id = cell[0].get_attribute("innerHTML")
                id = id.split()
                id = id[1]
                print(f'id: {id}')

                description = cell[1].get_attribute("innerHTML")
                description = description.split()
                description = " ".join(description)
                print(f'description: {description}')

                germanTargets[fields[s]][id] = {
                    "label": label,
                    "description": description,
                    "children": {}
                }
                
                for r,row in enumerate(rows[2:]):
                    #print(row.get_attribute("innerHTML"))
                    cells = row.find_elements("tag name", "td")

                    spans = cells[0].find_elements("tag name", "span")
                    idLevel1 = spans[0].get_attribute("innerHTML")
                    print(f'id: {idLevel1}')
                    label = spans[1].get_attribute("innerHTML")
                    print(f'label: {label}')
                    germanTargets[fields[s]][id]["children"][idLevel1] = {
                        "label": label,
                        "children": {}
                    }


                    for c,cell in enumerate(cells[1:]):
                        idTarget = idLevel1+letters[c]
                        print(f'id: {idTarget}')
                        #print(cell.get_attribute("innerHTML"))
                        try:
                            item = cell.find_element("class name", "competence-item-content")
                            label = item.find_element("class name", "ng-binding")
                            label = label.get_attribute("innerHTML")
                            print(f'label: {label}')

                            checkbox = False
                            #print(item.get_attribute("innerHTML"))
                            try:
                                item.find_element("class name", "checkbox")
                                checkbox = True

                            except:
                                print("No checkbox found..")
                            
                            germanTargets[fields[s]][id]["children"][idLevel1]["children"][idTarget] = {
                                "label": label,
                                "checked": checkbox
                            }

                        except:
                            print("No Target found..")
        #driverGerman.close() 
        return germanTargets
 

    except Exception as e:
        print(f"An Exception occurred {e}")

    finally:
        print("parse German closing...")
        driverGerman.close()
        #driver.close()
        
def compileJobId(text, i):
    text = text[0:4]
    id = "JB"+text+"{:03d}".format(i)
    return id

def parseMathSelectedTargets2(profile, url, jobId):
    letters = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E"
    }
    
    try:
        start_total = time.time()  # Start total time tracking
        driver.get(url) 
        # Time the retrieval of theme containers
        start = time.time()
        content = driver.find_elements("class name", "theme-container")
        end = time.time()
        print(f"Time to find theme containers: {end - start:.2f} seconds")
        
        for container in content:
            start = time.time()
            thema = container.find_element("class name", "theme-name")
            label_level0 = thema.text
            id_level0 = compileIdFromString(label_level0)
            print(id_level0)
            end = time.time()
            print(f"Time to process theme-name: {end - start:.2f} seconds")

            # Time to retrieve subtables
            start = time.time()
            subTables = container.find_elements("tag name", "table")
            end = time.time()
            print(f"Time to find subtables: {end - start:.2f} seconds")
            
            for table in subTables:
                # Time to process area titles and rows
                start = time.time()
                area = table.find_element("class name", "areaTitle")
                label_level1 = area.find_element("tag name", "td").text
                print("\t" + label_level1)
                id_level1 = compileIdFromString(label_level1)
                id_level1_con = id_level0 + id_level1
                print("\t" + id_level1_con)

                rows = table.find_elements("tag name", "tr")
                rows.pop(0)  # Remove the area title row
                end = time.time()
                print(f"Time to process area titles and rows: {end - start:.2f} seconds")
                
                for row in rows:
                    # Time to process each row
                    start = time.time()
                    elements = row.find_elements("tag name", "td")
                    rowName = elements[0].find_elements("tag name", "span")
                    id_level2 = rowName[0].text
                    id_level2_con = id_level1_con + id_level2
                    label_level2 = rowName[1].text
                    print("\t\t" + id_level2_con)
                    print("\t\t" + label_level2)
                    elements.pop(0)  # Remove the row name element

                    for i, element in enumerate(elements):
                        try:
                            # Time to find competence-item-content elements
                            start_inner = time.time()
                            subCells = element.find_elements("class name", "competence-item-content")
                            end_inner = time.time()
                            print(f"Time to find competence-item-content: {end_inner - start_inner:.2f} seconds. Nitems {len(subCells)}")
                            
                            for j, cell in enumerate(subCells):
                                start_checkbox = time.time()
                                print(cell.get_attribute("innerHTML"))
                                try:
                                    cell.find_element("class name", 
                                                                 "checkbox-container")
                                    id_level3 = letters[i] + str(j + 1)
                                    id_level3_con = id_level2_con + id_level3
                                    if id_level3_con not in profile:
                                        profile[id_level3_con] = []
                                    profile[id_level3_con].append(jobId)
                                    print("In profile: " + id_level3_con)
                                except NoSuchElementException:
                                    print("no checkbox")
                                end_checkbox = time.time()
                                print(f"Time to find checkbox: {end_checkbox - start_checkbox:.2f} seconds")

                        except NoSuchElementException:
                            print("No Element found...")
                    
                    end = time.time()
                    print(f"Time to process a row: {end - start:.2f} seconds")
                    
        end_total = time.time()
        print(f"Total execution time: {end_total - start_total:.2f} seconds")

        return profile

    except Exception as e:
        print(f"An Exception occurred {e}")
    
    finally:
        print("parse Math 2 closing...")
        driver.close()

def parseMathSelectedTargets(profile, url, jobId):
    letters = {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E"
        }
    try:
        driver = webdriver.Firefox()
        driver.implicitly_wait(2)

        driver.get(url)
        content = driver.find_elements("class name","theme-container")
        print("find element theme-container")
        print(f"length content {len(content)}")
        for container in content:
            thema = container.find_element("class name", "theme-name")
            print("find theme-name")
            label_level0 = thema.text
            id_level0 = compileIdFromString(label_level0)
            print(id_level0)

            subTables = container.find_elements("tag name", "table")
            
            for table in subTables:                
                area = table.find_element("class name", "areaTitle")
                label_level1 = area.find_element("tag name", "td").text
                print("\t"+label_level1)
                id_level1 = compileIdFromString(label_level1)
                id_level1_con = id_level0 + id_level1
                print("\t"+id_level0+id_level1)

                rows = table.find_elements("tag name", "tr")
                rows.pop(0) # get rid of first element, its the area Title
                
                ## Get Row Elements
                for row in rows:
                    elements = row.find_elements("tag name", "td")
                    rowName = elements[0]
                    rowName = rowName.find_elements("tag name", "span")
                    id_level2 = rowName[0].text
                    id_level2_con = id_level1_con + id_level2
                    label_level2 = rowName[1].text
                    print("\t\t"+id_level2_con)
                    print("\t\t"+label_level2)

                    elements.pop(0) #Get rid of row name
                    print(len(elements))
                    for i, element in enumerate(elements):
                        try:
                            subCells = element.find_elements("class name", "competence-item-content")
                            
                            for j, cell in enumerate(subCells):  
                                checkbox = cell.find_elements("class name", "checkbox-container")
                                if len(checkbox):
                                    id_level3 = letters[i]+str(j+1)
                                    id_level3_con = id_level2_con+id_level3
                                    if (id_level3_con not in profile):
                                        profile[id_level3_con] = []

                                    profile[id_level3_con].append(jobId)
                                    print("inn Profile: "+id_level3_con)
                            
                        except NoSuchElementException:
                            print("No Element found..")                            
                
        return(profile)
    except Exception as e:
        print(f"An Exception occurred {e}")

    finally:
        print("parse Math closing... ")
        driver.close() 

def goThruJoblist():

# Load the page

    jobs = {}
    i = 1
    with open("germanDep.json", "r") as infile:
        scrabbedAlready = json.load(infile)
    infile.close()
    for jobId in scrabbedAlready:
        print(jobId)
    
    links = {}
    german = scrabbedAlready
    try:
        driver.get('https://app-p-kompetenzraster.azurewebsites.net/#/')
        content = driver.find_elements("tag name","td")

        for row in content:
            job = row.find_element("tag name", "a")
            #print(job.get_attribute("innterHTML"))
            actions = ActionChains(driver)
            #actions.move_to_element(row).perform()
            #actions.scroll_to_element(row).perform()
            actions.scroll_by_amount(0,22).perform()
            #print(job.text)
            if job.text != "":
                jobId = compileJobId(job.text, i)
                url = job.get_attribute("href")  
                links[jobId] = url
                print(jobId)
                jobs[jobId] = job.text
                #table = job.click()
                #driver.implicitly_wait(5)
                i = i+1
                #driver.back()
                #driver.implicitly_wait(5)
        for jobId, url in links.items():
            print(jobId+" "+url)
            #profile = parseMathSelectedTargets(profile, url, jobId)
            if jobId not in scrabbedAlready:
                targets = parseGermanTargetsLabels(url)
                german[jobId] = targets
                with open("germanDep.json", "w") as outfile:
                    json.dump(german, outfile, indent = 4)
                outfile.close()
            #print(profile)
        """
        with open("jobIdsToJobNames.json", "w") as outfile:
            json.dump(jobs, outfile, indent=4)
        outfile.close() 
        print(jobs)

        with open("jobProfiles.json", "w") as outfile:
            json.dump(profile, outfile, indent=4)
        outfile.close() 
        print(jobs)
        """


    finally:
        print("go Thru Joblist closing...")
        driver.close()

if __name__ == "__main__":
    print("main")
    # Close the browser
    #url = 'https://app-p-kompetenzraster.azurewebsites.net/#/professionspublic/0ea79c50-f9dc-4760-b725-b357135d3db6'
    #parseGermanTargetsLabels(url)
    goThruJoblist()
    driver.quit()