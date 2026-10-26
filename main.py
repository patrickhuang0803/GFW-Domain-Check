#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from local_library import GfwCheck


if __name__ == "__main__":
    gc = GfwCheck()
    gc.check_ready_to_check_content("ready_to_check_fail_zones.txt")
    urls_list = gc.split_domains("ready_to_check_fail_zones.txt")
    browser = gc.browser_prepare()
    html_text = gc.htool_domains_check(browser, urls_list)
    check_results = gc.htool_html_text_resolve(html_text)
    print(check_results)