from flask import current_app
from elasticsearch import Elasticsearch
from config import Config
from flask import current_app as app
import requests
import json
from wordcloud import WordCloud
import operator
import os


class Article:

    def search(self, query, state, seen):
        results, dd = self.queryES(query,  seen)
        hits = []
        ids = []
        if results and 'hits' in results.keys():
            for hit in results['hits']['hits']:
                ids.append(hit['_id'])
                source = hit['_source']
                source['id'] = hit['_id']
                hits.append(source)

        nextState = int(state, 10) + \
            1 if type(state) == type(" ") else state + 1

        searchResults, sysOut = self.genSysOut(nextState, hits)

        try:
            self.genWordCloud(searchResults)
        except:
            pass

        return searchResults, '-1' if nextState >= 8 else str(nextState), sysOut

    def upvote(self, artile):
        pass
        # if not self.has_liked_post(post):
        #     like = PostLike(user_id=self.id, post_id=post.id)
        #     db.session.add(like)

    def unlike_post(self, article):
        pass
        # if self.has_liked_post(post):
        #     PostLike.query.filter_by(
        #         user_id=self.id,
        #         post_id=post.id).delete()

    def genSysOut(self, state, hits):
        if state == 0:
            return [], "Let's start..\n\nQ1: Name a digital world issue that interests you and why it interests you? " \
                "\nYou can be as descriptive as you wish. " \
                "There is no word limit. You can provide suggestive words, write in note form, or write full sentences."
        if state == 1:
            hits = hits[:5]
            concepts = self.getFeatures(hits, 'concept')
            categories = self.getFeatures(hits, 'category')
            return hits, "Do I understand you correctly? It appears you are keying in on issues related to:\n%s\n\n" \
                         "Your results fall into the following categories:\n%s\n\nWould you like to add more details?\n\t\t" \
                         "Choose 'Rephrase' after your edit, otherwise press 'Next'" % (
                             concepts, categories)
        if state == 2:
            hits = hits[:5]
            return hits, "Q2: Thinking about these articles, think about how your issue might manifest in the context of video-games and law? Now, please re-frame your issue so that it specifically applies in the context of video-games and the law."
        if state == 3:
            hits = hits[:10]
            concepts = self.getFeatures(hits, 'concept')
            categories = self.getFeatures(hits, 'category')
            return hits, "Do I understand you correctly? It appears you are keying in on issues related to:\n%s\n\n" \
                         "Your results fall into the following categories:\n%s\n\nWould you like to add more details?\n\t\t" \
                         "Choose 'Rephrase' after your edit, otherwise press 'Next' " % (
                             concepts, categories)
        if state == 4:
            hits = hits[:10]
            return hits, "Q3: Thinking about your video game law issue in the context of these new articles, can you re-frame your issue in an intellectually responsible manner with further precision and discipline as a question in under 25 words?"
        if state == 5:
            hits = hits[:15]
            concepts = self.getFeatures(hits, 'concept')
            categories = self.getFeatures(hits, 'category')
            return hits, "Do I understand you correctly? It appears you are keying in on issues related to:\n%s\n\n" \
                         "Your results fall into the following categories:\n%s\n\nWould you like to add more details?\n\t\t" \
                         "Choose 'Rephrase' after your edit, otherwise press 'Next'" % (
                             concepts, categories)
        if state == 6:
            hits = hits[:15]
            return hits, "Q4: Write an exploration up to 200 words illustrating two conflicting legal perspectives of your video game law topic referring to the assumptions underlying each perspective"
        if state == 7:
            hits = hits[:20]
            concepts = self.getFeatures(hits, 'concept')
            categories = self.getFeatures(hits, 'category')
            return hits, "Do I understand you correctly? It appears you are keying in on issues related to:\n%s\n" \
                         "Your results fall into the following categories:\n%s\n\nWould you like to add more details?\n\t\t" \
                         "Choose 'Rephrase' after your edit, otherwise press 'Next'" % (
                             concepts, categories)
        # if state == 8:
        #     hits = hits[:20]
        #     return hits, "Q5: With no word minimum or maximum talk about what you have learned (through research, in-class and otherwise) about your video game law topic. Summarize anything you feel has not been dealt with and/or resolved. With these in mind state five (5) questions related to your topic that could fruitfully be explored further. "
        if state == 8:
            hits = hits[:30]
            return hits, "There is no further clarification option. This is the end of the exercise."

        return [], "Please press Refresh button"

    def queryES(self, query, seen):
        ES = Config.ELASTICSEARCH_URL

        if len(seen) >= 1 and seen[-1] == ',':
            seen = seen[:-1]
        seen = '[' + seen + ']'

        query = query.replace("I need to know about", "")
        query = query.replace("I want information on", "")
        query = query.replace("?", "")

        data = """{
            "size": 30,
            "sort": [
                "_score",
                {"source_weight": "desc"}
            ],
            "query": {
                "bool": {
                    "must": {
                        "bool": {
                            "should": [

                                {
                                    "match": {
                                        "title": {
                                            "query": "%s",
                                            "boost": 6
                                        }
                                    }
                                },
                                {
                                    "match": {
                                        "analyzed_text": {
                                            "query": "%s",
                                            "boost": 2
                                        }
                                    }
                                },
                                {
                                    "match": {
                                        "analyzed_concept": {
                                            "query": "%s",
                                            "boost": 1
                                        }
                                    }
                                },
                                {
                                    "match": {
                                        "analyzed_relations.type": {
                                            "query": "%s",
                                            "boost": 1
                                        }
                                    }
                                }

                            ],
                            "must_not" :{
                                "ids": {
                                "values": %s
                                }
                            }
                        }
                    }
                }
            }
        }""" % (query, query, query, query, seen)
        response = requests.post(url=ES + '/_search', data=data,
                                 headers={'Content-Type': 'application/json'})
        results = json.loads(response.text)
        return results, data

    def getFeatures(self, hits, mode):
        counter = {}
        result = []
        firsts = []
        flag = True
        for hit in hits:
            flag = True
            for concept in hit['analyzed_' + mode]:
                if flag:
                    firsts.append(concept)
                    flag = False
                counter[concept] = 1 if concept not in counter.keys(
                ) else counter[concept] + 1

        for concept in counter:
            if counter[concept] > 1:
                result.append(concept)

        # result = result if len(result) != 0 else firsts
        for entry in firsts:
            if entry not in result:
                result.append(entry)

        string = '\n   '.join(result)

        return '   ' + string if string != "" else "{}"

    def genWordCloud(self, results):
        if os.path.exists(os.path.join(os.getcwd(), 'app/static/wordcloud.png')):
            os.remove(os.path.join(os.getcwd(), 'app/static/wordcloud.png'))
        freq = {}

        for article in results:
            keywords = article['analyzed_keyword']
            freqPerArticle = {}
            for kw in keywords:
                freqPerArticle[kw['text']] = kw['count']
                if kw['text'] in freq.keys():
                    freq[kw['text']] += kw['count']

                else:
                    freq[kw['text']] = kw['count']

            wc = WordCloud(max_font_size=50, max_words=100, background_color="white").generate_from_frequencies(
                freqPerArticle)
            wc.to_file("app/static/wordcloud-%s.png" % article['id'])

        wordcloud = WordCloud(max_font_size=50, max_words=100,
                              background_color="white").generate_from_frequencies(freq)
        wordcloud.to_file("app/static/wordcloud.png")
