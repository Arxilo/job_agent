from jobspy import scrape_jobs

def buscar_ofertas():

    trabajos = scrape_jobs(
        site_name=["linkedin", "indeed"],
        search_term="data analyst",
        location="Colombia",
        results_wanted= 10,
        hours_old= 96
    )

    return trabajos