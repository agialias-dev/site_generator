import shutil, os, logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='/home/agialias/projects/site_generator/audit_logs/static_to_public.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s : %(message)s')

public = '/home/agialias/projects/site_generator/public'
static = '/home/agialias/projects/site_generator/static'

def delete_tree_contents(path):
    print("Emptying the public directory...")
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        logger.info(f'Deleting {file_path}')
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            logger.error('Failed to delete %s. Reason: %s' % (file_path, e))

def copy_all_to_dir(source, destination):
    for filename in os.listdir(source):
        source_file_path = os.path.join(source, filename)
        try:
            if os.path.isdir(source_file_path):
                logger.info(f"Creating {source_file_path} in {destination}")
                os.mkdir(f"{destination}/{filename}")
                logger.info("Entering recursion")
                recursive_destination = f"{destination}/{filename}"
                copy_all_to_dir(source_file_path, recursive_destination)
            elif os.path.isfile(source_file_path) or os.path.islink(source_file_path):
                logger.info(f"Moving {source_file_path} to {destination}")
                shutil.copy(source_file_path, destination)
        except Exception as e:
            print('Failed to copy %s. Reason: %s' % (source_file_path, e))
            logger.error('Failed to delete %s. Reason: %s' % (source_file_path, e))