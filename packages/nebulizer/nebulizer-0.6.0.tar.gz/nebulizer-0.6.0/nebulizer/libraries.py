#!/usr/bin/env python
#
# libraries: functions for managing data libraries
import logging
import os
import fnmatch
from .core import get_current_user
from .core import Reporter
from bioblend import galaxy
import logging

logger = logging.getLogger(__name__)

def list_data_libraries(gi,long_listing_format=False,show_id=False):
    """
    Return list of data libraries

    Arguments:
      gi (bioblend.galaxy.GalaxyInstance): Galaxy instance
      long_listing_format (boolean): if True then use a
        long listing format when reporting items
      show_id (boolean): if True then also report the
        internal Galaxy IDs for data library items

    """
    output = Reporter()
    libraries = sorted(galaxy.libraries.LibraryClient(gi).get_libraries(),
                       key=lambda lib: lib['name'])
    for lib in libraries:
        display_items = [lib['name']]
        if long_listing_format:
            if lib['description']:
                description = "'%s'" % lib['description']
            else:
                description = "[No description]"
            display_items.append(description)
        if show_id:
            display_items.append(lib['id'])
        output.append(display_items)
    output.report()
    print("total %d" % output.nlines)

def library_id_from_name(gi,library_name):
    """
    Fetch ID for data library from library name

    Arguments:
      gi (bioblend.galaxy.GalaxyInstance): Galaxy instance
      library_name (str): name of data library to look up

    Returns:
      str: ID for data library, or None if name not found.

    """
    try:
        return galaxy.libraries.LibraryClient(gi).get_libraries(
            name=library_name)[0]['id']
    except IndexError:
        return None

def folder_id_from_name(gi,library_id,folder_name):
    """
    Fetch ID for folder

    Arguments:
      gi (bioblend.galaxy.GalaxyInstance): Galaxy instance
      library_id (str): ID for parent data library
      folder_name (str): name of folder to look up

    Returns:
      str: ID for folder, or None if name not found.

    """
    lib_client = galaxy.libraries.LibraryClient(gi)
    folder_name = normalise_folder_path(folder_name)
    logger.debug("Looking for '%s' in library %s" % (folder_name,
                                                      library_id))
    for folder in lib_client.get_folders(library_id):
        logger.debug("Checking '%s'" % folder['name'])
        if folder['name'] == folder_name:
            return folder['id']
    return None

def list_library_contents(gi,path,long_listing_format=False,
                          show_id=False):
    """
    Print contents of folder in data library

    The output of this function is loosely based on the
    output from the Linux `ls` command, and depends on
    what data items the input path (which can include
    wildcards).

    Arguments:
      gi (bioblend.galaxy.GalaxyInstance): Galaxy instance
      path (str): path describing a data library or
        a folder in a library
      long_listing_format (boolean): if True then use a
        long listing format when reporting items
      show_id (boolean): if True then also report the
        internal Galaxy IDs for data library items

    """
    # Get name and id for parent data library
    logger.debug("Path '%s'" % path)
    lib_client = galaxy.libraries.LibraryClient(gi)
    library_name,folder_path = split_library_path(path)
    logger.debug("library_name '%s'" % library_name)
    library_id = library_id_from_name(gi,library_name)
    if library_id is None:
        print("No library '%s'" % library_name)
        return
    # Get library contents
    library_contents = lib_client.show_library(library_id,contents=True)
    logger.debug("folder_path '%s'" % folder_path)
    # Bioblend class for getting more info for datasets if
    # using a long listing format
    dataset_client = galaxy.datasets.DatasetClient(gi)
    # Determine if we're matching against a wildcard pattern
    pattern = folder_path
    wildcard_pattern = False
    for c in "*?[]":
        try:
            pattern.index(c)
            wildcard_pattern = True
        except ValueError:
            pass
    # Output mode depends on whether we have wildcards
    if not wildcard_pattern:
        output = Reporter()
        # Exact matches only
        matches = [x for x in library_contents if x['name'] == pattern]
        if not matches:
            logger.error("Cannot access %s: no matching libraries "
                         "or folders" % path)
            return
        for item in matches:
            if item['type'] == 'folder':
                contents = [x for x in library_contents if
                            os.path.split(x['name'])[0] == item['name']]
            else:
                contents = matches
        # Remove 'root' folder
        contents = [x for x in contents if x['name'] != '/']
        for item in contents:
            if item['type'] == 'folder':
                output.append(report_folder(
                    lib_client.show_folder(library_id,
                                           item['id']),
                    long_listing=long_listing_format,
                    show_id=show_id))
            else:
                output.append(report_dataset(
                    item['id'],
                    dataset_client.show_dataset(item['id'],
                                                hda_ldda='ldda'),
                    long_listing=long_listing_format,
                    show_id=show_id))
        # Report
        output.report()
        print("total %s" % len(contents))
    else:
        output = Reporter()
        # Number of levels to match
        nlevels = pattern.count('/')
        # Mixture of matches possible
        matches = [x for x in library_contents
                   if (fnmatch.fnmatch(x['name'],pattern) and
                       x['name'].count('/') == nlevels)]
        if not matches:
            logger.error("Cannot access %s: no matching libraries "
                         "or folders\n" % path)
            return
        # Identify the folders that are matched exactly
        folders = []
        for item in matches:
            if item['type'] == 'folder' and item['name'] != '/':
                folders.append(item)
        # Locate non-folder items that are not in any of
        # the folders previously identified
        datasets = []
        for item in matches:
            implicit_dataset = False
            if item['type'] == 'folder':
                continue
            else:
                parent = os.path.split(item['name'])[0]
                for folder in folders:
                    if folder['name'] == parent:
                        #print("Parent = %s" % parent)
                        implicit_dataset = True
                        break
            # Item outside of folders
            if not implicit_dataset:
                datasets.append(item)
        # List the contents of each folder
        for folder in folders:
            output = Reporter()
            print("\n%s:" % folder['name'])
            folder_contents = [x for x in library_contents if
                               os.path.split(x['name'])[0] == folder['name']]
            for item in folder_contents:
                if item['type'] == 'folder':
                    output.append(report_folder(
                        lib_client.show_folder(library_id,
                                               item['id']),
                        long_listing=long_listing_format,
                        show_id=show_id))
                else:
                    output.append(report_dataset(
                        item['id'],
                        dataset_client.show_dataset(item['id'],
                                                    hda_ldda='ldda'),
                        long_listing=long_listing_format,
                        show_id=show_id))
            # Output to stdout
            output.report()
            if long_listing_format:
                print("total %s" % len(folder_contents))
        # List the datasets
        if datasets:
            print("\n.:")
            output = Reporter()
            for dataset in datasets:
                output.append(report_dataset(
                    item['id'],
                    dataset_client.show_dataset(item['id'],
                                                hda_ldda='ldda'),
                    long_listing=long_listing_format,
                    show_id=show_id))
            output.report()
            print("total %s" % len(datasets))

def create_library(gi,name,description=None,synopsis=None):
    """
    Create a new data library

    Arguments:
      gi (bioblend.galaxy.GalaxyInstance): Galaxy instance
      name (str): name of the new data library
      description (str): (optional) text to add as the
        description of the new data library
      synopsis (str): (optional) short 'synopsis' text
        to associate with the library

    Returns:
      str: id for data library.

    """
    lib_client = galaxy.libraries.LibraryClient(gi)
    if library_id_from_name(gi,name):
        print("Target data library already exists")
        return library_id_from_name(gi,name)
    library = lib_client.create_library(name,
                                        description=description,
                                        synopsis=synopsis)
    #print("%s" % library)
    return library['id']

def create_folder(gi,path,description=None):
    """
    Create a new folder in a data library

    Arguments:
      gi (bioblend.galaxy.GalaxyInstance): Galaxy instance
      path (str): path to the new folder (must be within
        an existing data library)
      description (str): text to add as the description
        of the new folder

    Returns:
      str: id for new folder.

    """
    # Break up the path
    library_name,folder_path = split_library_path(path)
    logger.debug("library_name: %s" % library_name)
    logger.debug("folder_path : %s" % folder_path)
    # Get name and id for parent data library
    lib_client = galaxy.libraries.LibraryClient(gi)
    library_id = library_id_from_name(gi,library_name)
    if library_id is None:
        print("Top level data library '%s' not found" % library_name)
        return None
    # Get folder name and base folder
    folder_base,folder_name = os.path.split(folder_path)
    # Check folder with same name doesn't already exist
    folder_id = folder_id_from_name(gi,library_id,folder_path)
    #print("folder_id '%s' for '%s'" % (folder_id,folder_path))
    if folder_id_from_name(gi,library_id,folder_path):
        print("Target folder already exists")
        return None
    #print("folder_name '%s' folder_base '%s'" % (folder_name,
    #                                             folder_base))
    base_folder_id = folder_id_from_name(gi,library_id,folder_base)
    #print("base_folder_id %s" % base_folder_id)
    new_folder = lib_client.create_folder(library_id,folder_name,
                                          description=description,
                                          base_folder_id=base_folder_id)
    #print("%s" % new_folder)
    return new_folder[0]['id']

def add_library_datasets(gi,path,files,
                         from_server=False,
                         link_only=False,
                         file_type='auto',
                         dbkey='?'):
    """
    Add datasets to a data library

    Note that the Galaxy instance must be associated with a
    real user in order to upload data; 'userless' instances
    (for example if using the master API) will be refused.

    Arguments:
      gi (bioblend.galaxy.GalaxyInstance): Galaxy instance
      path (str): path of folder to add datasets to
        files (list): list of files to upload to the data
        library
      from_server (bool): set True if files to be added are
        on the Galaxy server filesystem (default is False
        i.e. files on the local file system)
      link_only (bool): for files on the Galaxy server
        filesystem, set True to create links to the files
        (default is False i.e. copy files into Galaxy)
      file_type (str): explicit Galaxy file type to apply
        to all uploaded files (default is 'auto')
      dbkey (str): explicit dbkey to apply to all uploaded
        files (default is '?')

    """
    # Check that we're not using a 'userless' API key (e.g.
    # master key)
    if get_current_user(gi) is None:
        logger.error("No user associated with this API key, "
                     "data upload aborted")
        return
    # Break up the path
    library_name,folder_path = split_library_path(path)
    # Get name and id for parent data library
    lib_client = galaxy.libraries.LibraryClient(gi)
    library_id = library_id_from_name(gi,library_name)
    print("Library name '%s' id '%s'" % (library_name,library_id))
    # Get id for parent folder
    folder_id = folder_id_from_name(gi,library_id,folder_path)
    print("Folder name '%s' id '%s'" % (folder_path,folder_id))
    if from_server:
        # Assume that files are on Galaxy fileserver not localhost
        filesystem_paths = '\n'.join(files)
        print("Uploading files from Galaxy server:")
        print("%s" % filesystem_paths)
        lib_client.upload_from_galaxy_filesystem(
            library_id,filesystem_paths,
            folder_id=folder_id,
            file_type=file_type,
            dbkey=dbkey,
            link_data_only=link_only,
            roles='')
    else:
        # Files are on localhost
        for f in files:
            print("Uploading file '%s'" % f)
            lib_client.upload_file_from_local_path(
                library_id,f,
                folder_id=folder_id,
                file_type=file_type,
                dbkey=dbkey)

def split_library_path(path):
    """
    Split library path into library and folder components

    Note that the folder path will be returned as the
    normalised path i.e. /path/to/folder (single leading
    slash with no trailing slash).

    Arguments:
      path (str): path describing a folder in a data library

    Returns:
      Tuple: (library_name,folder_name)

    """
    components = path.strip('/').split('/')
    library_name = components[0]
    if len(components) == 1:
        folder_name = ''
    else:
        folder_name = '/'.join(components[1:])
    return (library_name,
            normalise_folder_path(folder_name))

def normalise_folder_path(path):
    """
    Normalise a folder path

    Normalise folder paths so that they are always of the
    form

    /path/to/folder

    i.e a single leading slash with no trailing slash

    Arguments:
      path (str): path for a data library folder

    Returns:
      str: normalised folder path.

    """
    return  '/'+'/'.join([x for x in path.split('/') if x != ''])

def report_folder(folder_data,long_listing=False,show_id=False):
    """
    Report details of a library folder

    Arguments:
      folder_data (dict): dictionary returned from an
        appropriate call to bioblend
      long_listing_format (boolean): if True then use a
        long listing format when reporting items
      show_id (boolean): if True then include the ID

    """
    logger.debug("%s" % folder_data)
    display_items = ["%s/" % folder_data['name'],
                     "folder"]
    if long_listing:
        if folder_data['description']:
            description = "'%s'" % folder_data['description']
        else:
            description = "[No description]"
        item_count = folder_data['item_count']
        display_items.extend([description,
                              "%d item%s" % (item_count,
                                             's' if item_count != 1
                                             else '')])
    if show_id:
        display_items.append(folder_data['id'])
    return display_items

def report_dataset(dataset_id,dataset_data,long_listing=False,
                   show_id=False):
    """
    Report details of a library dataset

    Arguments:
      dataset_data (dict): dictionary returned from an
        appropriate call to bioblend
      long_listing_format (boolean): if True then use a
        long listing format when reporting items
      show_id (boolean): if True then include the ID

    """
    logger.debug("%s" % dataset_data)
    display_items = [dataset_data['name'],
                     dataset_data['file_ext']]
    if long_listing:
        file_size = display_file_size(dataset_data['file_size'])
        display_items.extend([dataset_data['genome_build'],
                              file_size,
                              dataset_data['file_name']])
    if show_id:
        display_items.append("LLDA:%s" % dataset_id)
    return display_items

def display_file_size(file_size):
    """
    Convert a file size in bytes to a human-readable format e.g '5.6K'
    """
    units = ('K','M','G','T')
    if file_size < 1024:
        return "%d" % file_size
    for unit in units:
        file_size = float(file_size)/1024.0
        if file_size < 1024:
            break
    return "%.1f%s" % (file_size,unit)
