from __future__ import print_function
import json, csv
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions, ConceptsOptions, RelationsOptions, SemanticRolesOptions
import requests
import config


dir = '../resources/excels'
ES = config.Config.ELASTICSEARCH_URL
analyzed_fields = ['categories','concepts', 'entities', 'relations', 'semantic_role', 'keywords']
def analyze(url):
    service = NaturalLanguageUnderstandingV1(
        version=config.Config.IBM_VERSION,
        ## url is optional, and defaults to the URL below. Use the correct URL for your region.
        url=config.Config.IBM_URL,
        iam_apikey=config.Config.IBM_API_KEY)

    response = service.analyze(
        url=url,
        # text='what is the application of NLP in web page search?',
        features=Features(categories=CategoriesOptions(),
                          concepts=ConceptsOptions(limit=10),
                          entities=EntitiesOptions(),
                          relations=RelationsOptions(),
                          semantic_roles=SemanticRolesOptions(),
                          keywords=KeywordsOptions()
                          ),
        return_analyzed_text=True,
        clean=True
    ).get_result()

    return response

    # print(json.dumps(response, indent=2))


def getSourceWeight(url):
    if 'arstechnica.com' in url:
        return 14
    if 'michaelgeist.ca' in url:
        return 18
    if 'blog.ericgoldman.org' in url:
        return 16
    if 'techdirt.com' in url:
        return 15
    if 'gamasutra.com' in url:
        return 10
    if 'gamesindustry.biz' in url:
        return 12
    return 10

counter = 0
with open(dir + '\\' + 'all.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        counter += 1
        print(counter)

        data = {
            'title' : row[0],
            'url' : row[1],
            'course_topic': row[2],
            'upvote': 0,
            'downvote': 0,
            'analyzed_category' : [],
            'analyzed_concept': [],
            'analyzed_entity': [],
            'analyzed_relations': [],
            'analyzed_sem_rol': [],
            'analyzed_keyword': []
        }
        try:
            analyzed = analyze(url=row[1])


            data['analyzed_text'] = analyzed['analyzed_text']

            data['analyzed_keyword'] = analyzed['keywords']

            for category in analyzed['categories']:
                data['analyzed_category'].append(category['label'])

            for concept in analyzed['concepts']:
                data['analyzed_concept'].append(concept['text'])

            for entity in analyzed['entities']:
                data['analyzed_entity'].append({'text': entity['text'], 'type': entity['type']})

            for relation in analyzed['relations']:
                data['analyzed_relations'].append(relation)

            for sem_rol in analyzed['semantic_roles']:
                data['analyzed_sem_rol'].append(sem_rol)

            data['source_weight'] = getSourceWeight(row[1])
            data['upvote'] = 0
            data['downvote'] = 0
            data['upvote_voters'] = []
            data['downvote_voters'] = []

        except Exception:
            print("Faild to analyze ", row)
            pass

        post2ES = requests.post(url=ES+'articles/_doc', data=json.dumps(data, indent=2), headers={'Content-Type': 'application/json'})
        print(post2ES.content)
