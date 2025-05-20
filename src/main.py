from textnode import *
from htmlnode import *
from inline_functions import *
from block_functions import *
from final_functions import *
from file_functions import *

def main():
    delete_tree_contents(public)
    copy_all_to_dir(static, public)
    logger.info("Task completed.")
    generate_pages_recursively("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()