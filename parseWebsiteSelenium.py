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
        print("closing...")
        driver.close()

#parseMathTargetsLabels()

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
    
    finally:
        print("closing...")
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

        print("closing... ")
        driver.close() 

def goThruJoblist():
# Load the page
    jobs = {}
    i = 1
    profile = {}
    links = {}
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
            profile = parseMathSelectedTargets(profile, url, jobId)
            print(profile)

        with open("jobIdsToJobNames.json", "w") as outfile:
            json.dump(jobs, outfile, indent=4)
        outfile.close() 
        print(jobs)

        with open("jobProfiles.json", "w") as outfile:
            json.dump(profile, outfile, indent=4)
        outfile.close() 
        print(jobs)


    finally:
        print("closing...")
        driver.close()

goThruJoblist()

# Close the browser
driver.quit()