import json
import os

path = 'films/'
movie_number = 0
crew_number = 0
director_number = 0
writer_number = 0
studio_number = 0
part2 = ''
part3 = ''
part5 = ''
part4 = ''
directors = dict()
writers = dict()
crews = dict()
studios = dict()


def movie_id():
    return 'movie_' + str(movie_number)


def crew_id():
    return 'crew_' + str(crew_number)


def director_id():
    return 'director_' + str(director_number)


def writer_id():
    return 'writer_' + str(writer_number)


def studio_id():
    return 'studio_' + str(studio_number)


# individual declaration
def individual_declaration(id):
    return '<Declaration>\n\t<NamedIndividual IRI="#' + str(id) + '"/>\n</Declaration>\n'


# define individual type
def define_individual_type(type, id):
    return '<ClassAssertion>\n\t<Class IRI="#' + type + '"/>\n\t<NamedIndividual IRI="#' + str(
        id) + '"/>\n</ClassAssertion>\n'


# data property assertion
def data_property_assertion(property, id, value):
    if property == 'genre':
        value = ', '.join(value)
    return '<DataPropertyAssertion>\n\t<DataProperty IRI="#' + property + '"/>\n\t<NamedIndividual IRI="#' + str(
        id) + '"/>\n\t<Literal>' + value + '</Literal>\n</DataPropertyAssertion>\n'


def object_property_assertion(property, id1, id2):
    return '<ObjectPropertyAssertion>\n\t<ObjectProperty IRI="#' + property + '"/>\n\t<NamedIndividual IRI="#' + str(
        id1) + '"/>\n\t<NamedIndividual IRI="#' + str(id2) + '"/>\n</ObjectPropertyAssertion>\n'


for file in os.listdir(path):
    with open(path + file, 'r') as f:
        data = json.load(f)
        part2 += individual_declaration(movie_id())
        part3 += define_individual_type('Movie', movie_id())
        for property, value in data.items():
            if not value:
                continue
            if property == 'Directed By':
                for director in value.split(','):
                    if director in directors:
                        part4 += object_property_assertion('DirectedBy', movie_id(), directors[director])
                    elif director in writers:
                        part4 += object_property_assertion('DirectedBy', movie_id(), writers[director])
                    else:
                        directors[director] = director_id()
                        part2 += individual_declaration(director_id())
                        part3 += define_individual_type('Director', director_id())
                        part4 += object_property_assertion('DirectedBy', movie_id(), director_id())
                        part5 += data_property_assertion('firstName', director_id(), director.split(' ')[0])
                        if len(director.split(' '))>1:
                            part5 += data_property_assertion('lastName', director_id(), director.split(' ')[1])
                        director_number += 1
            elif property == 'Written By' and value != '':
                for writer in value.split(','):
                    if writer in writers:
                        part4 += object_property_assertion('WritedBy', movie_id(), writers[writer])
                    else:
                        writers[writer] = writer_id()
                        part2 += individual_declaration(writer_id())
                        part3 += define_individual_type('MovieWriter', writer_id())
                        part4 += object_property_assertion('WritedBy', movie_id(), director_id())
                        part5 += data_property_assertion('firstName', writer_id(), writer.split(' ')[0])
                        if len(writer.split(' ')) >1:
                            part5 += data_property_assertion('lastName', writer_id(), writer.split(' ')[1])
                        writer_number += 1
            elif property == 'Studio':
                if value in studios:
                    part4 += object_property_assertion('ProducedBy', movie_id(), studios[value])
                else:
                    studios[value] = studio_id()
                    part2 += individual_declaration(studio_id())
                    part3 += define_individual_type('Studio', studio_id())
                    part4 += object_property_assertion('ProducedBy', movie_id(), studio_id())
                    part5 += data_property_assertion('name', studio_id(), value)
                    studio_number += 1
            elif property == 'crew':
                for crew in value:
                    if crew == {}:
                        pass
                    elif crew['first_name'] + ' ' + crew.get('last_name', '') in crews:
                        part4 += object_property_assertion('hasCrew', movie_id(),
                                                           crews[crew['first_name'] + ' ' + crew.get('last_name', '')])
                    elif crew['first_name'] + ' ' + crew.get('last_name', '') in directors:
                        part4 += object_property_assertion('hasCrew', movie_id(), directors[
                            crew['first_name'] + ' ' + crew.get('last_name', '')])
                    else:
                        crews[crew['first_name'] + ' ' + crew.get('last_name', '')] = crew_id()
                        part2 += individual_declaration(crew_id())
                        part3 += define_individual_type('Crew', crew_id())
                        part4 += object_property_assertion('hasCrew', movie_id(), crew_id())
                        part5 += data_property_assertion('pictureUrl', crew_id(), crew['img'])
                        part5 += data_property_assertion('lastName', crew_id(), crew.get('last_name', ''))
                        part5 += data_property_assertion('firstName', crew_id(), crew['first_name'])
                        birthday = crew.get('Birthday', 'Birthday\xa0\xa0' )
                        part5 += data_property_assertion('birthday', crew_id(), birthday)
                        birthplace = crew.get('Birthplace', 'Birthplace\xa0\xa0' )
                        part5 += data_property_assertion('birthPlace', crew_id(), birthplace)
                        crew_number += 1
            else:
                if 'In' not in property and 'On' not in property:
                    part5 += data_property_assertion(str.lower(property), movie_id(), value)
        movie_number += 1

with open('owls/part1.owl', 'r') as f:
    part1 = f.read()

with open('owls/part6.owl', 'r') as f:
    part6 = f.read()

with open('result_ontology.owl', 'w', encoding='utf8') as f:
    f.write(part1)
    f.write(part2)
    f.write(part3)
    f.write(part4)
    f.write(part5)
    f.write(part6)
print('finish!')