helpMsg = '''
    usage:
        python manage.py <command>

    commands:
        run: Start Web Server
        scrapStatus: Scrap Doctor Status from website
        scrapSchedule: Scrap Doctor Schedule from website
        clean: Clean Up Outdate Doctor Status and Schedule
        initDB: Create Tables in database
        dropDB: Remove Tables in database
    
    first run:
        run 'python manage.py dropDB initDB scrapStatus scrapSchedule'

        add to crontab:
            run 'python manage.py scrapStatus' per 3 minutes
            run 'python manage.py scrapSchedule clean' per day
        
        run python manage.py run
'''
def main():
    import sys
    if len(sys.argv) < 2:
        print(helpMsg)
        return
    for command in sys.argv[1:]:
        if command == 'run':
            from web import run
            run()
            continue
        if command == 'scrapStatus':
            from scraper import scrapStatus
            scrapStatus()
            continue
        if command == 'scrapSchedule':
            from scraper import scrapSchedule
            scrapSchedule()
            continue
        if command == 'clean':
            from scraper import clean
            clean()
            continue
        if command == 'initDB':
            from database.database import init_db
            from scraper import storeAllDepartment
            init_db()
            storeAllDepartment()
            continue
        if command == 'dropDB':
            from database.database import drop_db
            drop_db()
            continue
        print(helpMsg)
        return

if __name__ == "__main__":
    main()
