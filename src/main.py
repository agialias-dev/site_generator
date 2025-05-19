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
    generate_page("/home/agialias/projects/site_generator/content/index.md", "/home/agialias/projects/site_generator/template.html", "/home/agialias/projects/site_generator/public/index.html")

if __name__ == "__main__":
    main()