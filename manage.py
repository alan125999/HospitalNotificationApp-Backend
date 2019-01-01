helpMsg = '''
    usage:
        python manage.py <command>

    commands:
        run
        scrapStatus
        scrapSchedule
        initDB
        dropDB
'''
def main():
    import sys
    if len(sys.argv) < 2:
        print(sys.argv)
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
