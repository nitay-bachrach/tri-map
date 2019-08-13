import sheets
import locator
import conf
import simplekml
import exc

def get_location(loc_handler, place):
    print 'Locating %s' % place
    try:
        locations = loc_handler.get_location(place)
        if not locations:
            print 'failed, locating with London'
            locations = loc_handler.get_location('%s London' % place)
        return locations
    except exc.MapperException as e:
        print 'error', e.message
        return []


def create_kml(points, output):
    kml = simplekml.Kml()
    for name, location, desc in points:
        coords = [(location[0]['lng'], location[0]['lat'])]
        kml.newpoint(name=name, description=desc, coords=coords)
    kml.save(output)

def main():
    sheet_handler = sheets.Sheet()
    loc_handler = locator.Locator()
    results = sheet_handler.get_results(conf.DOC_ID, 'A2:END')
    print 'got results'
    points = [(result[0], get_location(loc_handler,result[0]), result[10]) for result in results if float(result[10])> conf.MIN_RATING]
    print 'got locations'
    located_points = []
    for point in  points:
        if not point[1]:
            print '%s is not located' % point[0]
        else:
            located_points.append(point)
    print 'creating kml'
    create_kml(located_points, conf.KML_OUTPUT)
    print 'done'

if __name__ == '__main__':
    main()
