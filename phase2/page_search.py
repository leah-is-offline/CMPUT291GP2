from state_machine import State
from util import promptForOption, inputIntRange
import db_search

page_size = 5

class Search(State):
    def run(self):
        from page_menu import Menu
        from page_view_post import ViewPost

        print("-- Search --")
        keywordsList = self.inputKeywords()
        results = db_search.getMatchingQuestions(keywordsList)

        page = 0

        while (True):
            pagePosts = self.displayPage(page, results)

            options = []
            #if this page has results
            if len(pagePosts) > 0:
                options.append(("View post", "view_post"))

                # if there are more results
                if len(results) > (page+1)*page_size:
                    options.append(("Next Page", "next_page"))
            else:
                print("\nNo results...")

            options += [
                ("Search again", "state", Search),
                ("Back to Menu", "state", Menu)
            ]

            choice = promptForOption(options)
            if (options[choice][1] == "state"):
                return options[choice][2]
            elif options[choice][1] == "next_page":
                page += 1
            elif options[choice][1] == "view_post":
                idx = inputIntRange("Which Post: ", 1, len(pagePosts))-1
                ViewPost.postId = pagePosts[idx]["Id"]
                return ViewPost


        return Search

    def inputKeywords(self):
        keywords = input("Enter one or more keywords (separated by a space): ")
        #function to validate user provided keywords, user must provide one or more
        while keywords.isspace() or len(keywords) == 0:
            print("Invalid Entry")
            keywords = input("Enter one or more keywords (separated by a space): ")
        validKeywordsList = list(keywords.split(" "))
        return validKeywordsList

    def displayPage(self, page, posts:list):
        from math import ceil
        global page_size
        pCount = len(posts)
        start = min(page * page_size, pCount)
        end = min(start + page_size, pCount)

        print("-------- Page {} of {} -----------"
              .format(page+1, ceil(pCount/page_size)))

        pagePosts = posts[start:end]
        for idx, post in enumerate(pagePosts, start=1):
            title = post["Title"]
            creationDate = post["CreationDate"]
            score = post["Score"]
            answerCount = post["AnswerCount"]
            print("{i}. Title: {title}"
                  .format(i = idx, title = title))
            print("Creation Date: {cd} | Score : {score} | AnswerCount {ac}\n"
                  .format(cd = creationDate, score = score, ac = answerCount))
        return pagePosts
