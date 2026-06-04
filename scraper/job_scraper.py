from jobspy import scrape_jobs

def buscar_ofertas(search_term , location):

    trabajos = scrape_jobs(
        site_name=["linkedin", "indeed"],
        search_term= search_term,
        location= location,
        results_wanted= 10,
        hours_old= 96
    )

    return trabajos