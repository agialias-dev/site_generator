import sys
from final_functions import *
from file_functions import *

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

def main():
    delete_tree_contents(docs)
    copy_all_to_dir(static, docs)
    logger.info("Task completed.")
    generate_pages_recursively("./content", "./template.html", docs)

if __name__ == "__main__":
    main()