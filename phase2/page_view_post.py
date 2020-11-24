from state_machine import State
import db
from util import inputInt, promptForOption, inputIntRange

page_size = 5

class ViewPost(State):
    # static variable
    postId = None
    def run(self):
        from page_menu import Menu
        from page_make_post import PostAnswer

        global postId
        if (ViewPost.postId == None):
            print('postId must be staticly defined to use this class!')
            return None

        print("-- Viewing post: %s --" % ViewPost.postId )

        #post = db.getPost(ViewPost.postId)
        post = db.viewPost(ViewPost.postId)
        for key, value in post.items():
            print('{:15} {}'.format(key+':', value))
        
        print("\n\nWhat would you like to do?")

        # Compose the list of user option / actions
        options = [
            ("Vote on post", "func", self.voteOnPost),
            ("Back to Menu", Menu)
        ]

        if post['PostTypeId'] == "1":
            PostAnswer.questionId = ViewPost.postId
            options[-1:-1] = [
                ("List answers", "func", self.showAnswers),
                ("Add an answer", PostAnswer)
            ]

        # Print the available options
        for i, option in enumerate(options, start=1):
            print(str(i)+ ". " + option[0] )
        print()

        # get user input
        choice = inputInt("Please select an option: ")
        while(choice < 1 or choice > len(options)):
            choice = inputInt("Not in range: ")

        # execute func or go to next state
        option = options[choice-1]
        if (option[1] == "func"):
            return option[2]()
        return option[1]

    def voteOnPost(self):
        db.insertVote(ViewPost.postId, "2")
        input("Press enter to continue")
        return ViewPost

    def showAnswers(self):
        #from page_menu import Menu #import here or Menu is undefined
        answers = db.getAnswers(ViewPost.postId)
        if len(answers) == 0:
            print("This questions has not been answered yet.")
            print("\n\nWhat would you like to do?")
            return self.Menu
        else:
            global page_size
            page = 0
            
            while True:
                
                pageAnswers = self.displayAnswerPage(page, answers)

                options = []
                if len(pageAnswers) > 0:
                    options.append(("View Answer", "view_answer"))
                    if len(answers) > (page+1)*page_size:
                        options.append(("Next Page", "next_page"))
                else:
                    print("\nNo Answers...")

            
                choice = promptForOption(options)
                if options[choice][1] == "next_page":
                    page += 1
                elif options[choice][1] == "view_answer":
                    idx = inputIntRange("Which Answer: ", 1, len(pageAnswers))-1
                    ViewPost.postId = pageAnswers[idx]["Id"]
                    
                    return ViewPost
            
            
    def displayAnswerPage(self, page, answers:list):
        from math import ceil
        global page_size

        pCount = len(answers)
        start = min(page * page_size, pCount)
        end = min(start + page_size, pCount)

        print("-------- Page {} of {} -----------"
              .format(page+1, ceil(pCount/page_size)))


        pageAnswers = answers[start:end]
        for idx, answer in enumerate(pageAnswers, start=1):
            body = answer["Body"] 
            body = body[:min(len(body), 80)] + "..."
            creationDate = answer["CreationDate"]
            score = answer["Score"] 

    
            print("{i}. Body: {body}"
                  .format(i = idx, body = body))
            print("Creation Date: {cd} | Score : {score}\n"
                  .format(cd = creationDate, score = score))
        return pageAnswers
            
