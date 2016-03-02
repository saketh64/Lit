import re

# pattern to parse artist and title from a youtube video title
PARSE_PATTERN = "([^\r\n-]{1,}) - ([^-\r\n]{1,})"

# pattern to parse modifiers, e.g. "(Official Video) or [2016]"
MODIFIER_PATTERN = "(\(.*?\)|\[.*?\])"

def remove_modifiers(youtube_title):
    """Removes things like "(Official album version)" from a youtube title
    (basically removes anything in parentheses)
    """
    return re.sub(MODIFIER_PATTERN,'',youtube_title)

def format(youtube_title):
    """Just some basic whitespace formatting"""
    youtube_title = youtube_title.replace('  ',' ')
    youtube_title = youtube_title.strip()
    return youtube_title

def try_parse(youtube_title):
    """Tries to parse an artist/title out of the given youtube title

    :param youtube_title: str
    :return: tuple -> (artist,title) or (None,None)
    """
    youtube_title = format(remove_modifiers(youtube_title))

    result = re.match(PARSE_PATTERN,youtube_title)
    if result != None:
        artist = result.group(1)
        title = result.group(2)
        return format(artist),format(title)
    else:
        return None,None


def can_add(results,new_result):
    """If there's already a search result with the same artist/title, we can't add this new result - it's a duplicate

    :param results: list of YoutubeSearchResult objects
    :param new_result: a singl YoutubeSearchResult that we'd like to add
    :return: boolean
    """

    # This 'if' checks artist and title equality. see YoutubeSearchResult.__eq__
    if new_result in results:
        return False

    # Same check after swapping artist and title - in case the parsing was incorrect
    # e.g. "Childish Gambino - Sober" vs "Sober - Childish Gambino" - same song.
    new_result.artist,new_result.title = new_result.title,new_result.artist
    if new_result in results:
        return False

    # undo the swap, since we're going to use this YoutubeSearchResult in the list
    new_result.artist,new_result.title = new_result.title,new_result.artist

    return True


def filter_results(results):
    """This is the MAIN filtering method.

    Filtering essentially does two thigns currently:
        Avoids adding duplicate songs if possible
        Pushes results with weird titles to the bottom of the list
            (these tend to be interviews and other things like that)

    :param results: list of YoutubeSearchResult objects
    :return: The filtered list of results
    """

    # these will be appended to the bottom of the list at the end
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
                # duplicate song!
                print "Skipping '"+result.youtube_title+"'"
        else:
            # couldn't parse artist and title
            unparsed_results.append(result)

    # append results with weird titles to the end
    filtered_results += unparsed_results

    return filtered_results
