import re

# pattern to parse artist and title from a youtube video title
PARSE_PATTERN = "([^\r\n-]{1,}) - ([^-\r\n]{1,})"

# pattern to parse modifiers, e.g. "(Official Video)"
MODIFIER_PATTERN = "\(.*?\)"

def remove_modifiers(line):
    return re.sub(MODIFIER_PATTERN,'',line)

def format(line):
    line = line.replace('  ',' ')
    line = line.strip()
    return line

def try_parse(line):
    result = re.match(PARSE_PATTERN,line)
    if result != None:
        artist = result.group(1)
        title = result.group(2)

        title = remove_modifiers(title)
        return format(artist),format(title)
    else:
        return None,None


def can_add(results,new_result):
    if new_result in results:
        return False

    return True


def filter_results(results):
    unparsed_results = []
    filtered_results = []
    for result in results:
        artist,title = try_parse(result.youtube_title)
        if artist != None:
            result.song_title = title
            result.artist = artist

            if can_add(filtered_results,result):
                filtered_results.append(result)

            else:
                print "Skipping '"+result.youtube_title+"'"
        else:
            unparsed_results.append(result)

    filtered_results += unparsed_results

    return filtered_results
