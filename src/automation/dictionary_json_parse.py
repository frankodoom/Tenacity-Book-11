
# %%
import json


JSONPATH ="../app/dictionary-popup/dictionary.json"
TENACITYBOOK10_JSONPATH = r"C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book10\src\app\dictionary-popup\dictionary.json"
print(TENACITYBOOK10_JSONPATH)
# with open(TENACITYBOOK10_JSONPATH, "r", encoding="utf-8") as jsonfile:
#     output = json.load(jsonfile)

# words : list[str] = []

# for i in output :
#     if output[i]['entries'] != []:
#        words.append(i)

# words.sort(key = lambda x: len(x) )
# print(words)
# lenOfwords = len(words)

# actual_list = list(range(lenOfwords))
# range_words = range(lenOfwords)
# nested_words = set()
# final_dict = dict()
# for i in range_words :
#     cur_word = words[i]
#     modified = actual_list.copy()
#     del modified[i]
#     final_dict.update({cur_word: []})

#     for j in modified:
#         cur_test_word = words[j]
#         if cur_test_word  in cur_word:
#             final_dict[cur_word].append(cur_test_word)
#             nested_words.add(cur_test_word)



# # %%
# overrall_nest_dict = {}
# for word in words:
#     #word_to_remove = []
#     word_dict_arr = { word : []}
#     #arr_appended = False

#     wordsCopy = words.copy()
#     wordsCopy.remove(word);
#     for wordnest in wordsCopy:

#         if word in wordnest:
#             word_dict_arr[word].append(wordnest)
#             #word_to_remove.append(wordnest)
#             #arr_appended = True

#     if word_dict_arr[word] != []:
#         overrall_nest_dict.update(word_dict_arr)

# subnesting_dict = { i : overrall_nest_dict[i] for i in filter( lambda x: len(overrall_nest_dict[x]) > 1 , overrall_nest_dict) }
# subnesting_dict_new = subnesting_dict.copy()

# for i in subnesting_dict:

#     words_to_loop = subnesting_dict[i]
#     subword_dict_store = {}
#     for word in words_to_loop:
#         #word_to_remove = []
#         word_dict_arr = { word : [] }
#         wordsCopy = words_to_loop.copy()
#         wordsCopy.remove(word)
#         for wordnest in wordsCopy:
#             if word in wordnest:
#                 word_dict_arr[word].append(wordnest)

#         if word_dict_arr[word] != []:
#               subword_dict_store.update(word_dict_arr)

#     if subword_dict_store != {} :
#         subnesting_dict_new.update({i : subword_dict_store} )








# %%

def listWord_to_dictWords ( listOfWords : list[str], level = 1):
    """
      Goes through an array of words and creates a tree, the structure of the tree will indicate which
      word contains other words, Eg: [eat , at] will result in {at : ["eat"]} because eat contains at,
      if non of the words contain eachother, the array will just be returned

      !!! IMPORTANT !!! sort the words by len (smallest at index 0)
    """
    shouldRecurse = False
    sorted_words = listOfWords.copy()
    thedictoutput = {}
    overrall_matched_nestedwords = []
    flat_array = []
    for word in sorted_words:
        nestedWordsList = []

        if word in overrall_matched_nestedwords:
            continue

        modifieable = sorted_words.copy()
        modifieable.append("empty") # For padding sake, this is here due to slice ignoring last index item
        word_index = modifieable.index(word)
        #print("Modifiable" ,modifieable[word_index+1 : -1])
        for nestWord in modifieable[word_index+1 : -1]:
            if word in nestWord:
                nestedWordsList.append(nestWord )
                ## Array structure, first position is parent object, second position is item itself, third position is level
                flat_array.append( (level, nestWord, word ) )

        if len(nestedWordsList) >= 2 :
            shouldRecurse = True

        if nestedWordsList != []:
            thedictoutput.update({ word  : nestedWordsList})



        overrall_matched_nestedwords.extend(nestedWordsList)



    if shouldRecurse:
        for i in thedictoutput:
            thearr = thedictoutput[i]
            if len(thearr) >= 2:
                result = listWord_to_dictWords( thearr , level + 1 )
                if result[0] != {}:
                    thedictoutput[i] = result[0]
                    flat_array.extend(result[1])


    return thedictoutput , flat_array


# %%
# nested_search_word , arrangement = listWord_to_dictWords(words)

# %%
# def get_depth( dict_obj, key ):

#     out1 = dict_obj[key]
#     if isinstance(out1 , dict):
#         temp = 0
#         for i in out1.keys():
#             res =get_depth( out1, i)
#             temp = res  if res > temp else temp
#         return temp + 1
#     else:
#         return 1

# %%
#get_depth(nested_search_word, "source")


# %%
# Invert The Tree V1


# arrangement.sort( key = lambda x : x[0] , reverse = True)
# print(arrangement)

# unique_groups =  list({ i[0] for i in arrangement  })
# unique_groups.sort( reverse=True)
# print(unique_groups)

# result = { i : [d for d in arrangement if d[0] == i] for i in unique_groups  }
# result_len = len(result)
# new_form = [[None] * (result_len + 1)]


# arrays = [[]]*(result_len+1) ## Each Array From left to right is a column

# count = 1
# used_words_set = set()

# for level in range( result_len , 0, -1):
#     print(i)

#     current_array = result[level]
#     lenOf_current_array = len(current_array)

#     for ca_item in current_array:

#         repetition_found = False
#         for final_item in new_form:

#             # IF There is repetition in the same level
#             # FOR LOOP FOR CHECKING PREVIOUS LEVEL
#             for prv_levels in range( level , result_len + 1 ):

#                 if ca_item[1] == final_item[ result_len - level ]:
#                     repetition_found = True

#                     index_of_newform = new_form.index(final_item)

#                     temp_newform_subarray = new_form[index_of_newform]

#                     next_position = temp_newform_subarray[ result_len - (prv_levels - 1)]
#                     if ca_item[2] not in used_words_set:
#                       if next_position == None:
#                           new_form[index_of_newform][result_len - (prv_levels - 1)] = ca_item[2]
#                       elif isinstance(next_position,str):
#                           new_form[index_of_newform][result_len - (prv_levels- 1)] = [ next_position , ca_item[2]]
#                       elif isinstance(next_position, list):
#                           new_form[index_of_newform][result_len - (prv_levels- 1)].append( ca_item[2])
#                       used_words_set.add(ca_item[2])


#         if not repetition_found:
#             #Else create new item
#             temp = [None] * (result_len + 1)
#             if ca_item[1] not in used_words_set:
#               temp[result_len - (level )] = ca_item[1]
#             if ca_item[2] not in used_words_set:
#               temp[result_len - (level - 1)] = ca_item[2]
#             new_form.append(temp)
#             used_words_set.add(ca_item[1])
#             used_words_set.add(ca_item[2])




        # if ca_item[1] not in arrays[result_len- i]:
        #     arrays[result_len- i].append(ca_item[1])
        # else:
        #     index = arrays[result_len - i].index(ca_item[1])




        # for z in range(lenOf_current_array):
        #     if z == i:
        #         continue

        #     secondary_item = current_array[z]


# %%
# INVERT THE TREE V2
# arrangement.sort( key = lambda x : x[0] , reverse = True)
# print(arrangement)

# unique_groups =  list({ i[0] for i in arrangement  })
# unique_groups.sort( reverse=True)
# print(unique_groups)

# result = { i : [d for d in arrangement if d[0] == i] for i in unique_groups  }
# result_len = len(result)
# new_form = []


# arrays = [[]]*(result_len+1) ## Each Array From left to right is a column

# count = 1
# used_words_set = set()
# tracking_dict = {}

# for level in range( result_len , 0, -1):
#     print(i)

#     current_array = result[level]
#     lenOf_current_array = len(current_array)

#     for ca_item in current_array:

#         first_level_repetition_found = ca_item[1] in used_words_set
#         second_level_repetition_found = ca_item[2] in used_words_set

#         if not first_level_repetition_found and not second_level_repetition_found:
#             #Create New Row
#             #IF first level is not found, just add second level, whether its found or not
#             temp = [None] * (result_len +1 )
#             temp[ result_len - level ] = ca_item[1]
#             temp[ result_len - (level - 1)] = ca_item[2]

#             used_words_set.add(ca_item[1])
#             used_words_set.add(ca_item[2])

#             tracking_dict.update( { ca_item[1] : len(new_form) , ca_item[2] : len(new_form)} )

#             new_form.append(temp)

#         elif (first_level_repetition_found and not second_level_repetition_found) or (not first_level_repetition_found and second_level_repetition_found):
#             #Find The Row
#             the_index = -1
#             increment = 0
#             ca_item_index = 0
#             ca_next_item_index = 0
#             if(first_level_repetition_found and not second_level_repetition_found):
#                 ca_item_index = 1
#                 increment = 1
#             else:
#                 ca_item_index = 2
#                 increment = -1
#             the_index = tracking_dict[ca_item[ca_item_index]]
#             sub_array_temp = new_form[the_index]

#             for ind in range(3):
#                 cur_val = sub_array_temp[ind]
#                 ind_p1 = ind + increment
#                 if isinstance(cur_val, str) and cur_val == ca_item[ca_item_index]:
#                     next_val = sub_array_temp[ind_p1]
#                     if next_val == None:
#                         sub_array_temp[ind_p1] = ca_item[ca_item_index + increment]
#                     if isinstance(next_val, str):
#                         sub_array_temp[ind_p1] = [next_val , ca_item[ca_item_index + increment]]
#                     if isinstance(next_val, list):
#                         sub_array_temp[ind_p1].append(ca_item[ca_item_index + increment])
#                     new_form[the_index] = sub_array_temp
#                     tracking_dict.update( {ca_item[ca_item_index + increment] : the_index} )
#                     used_words_set.add(ca_item[ca_item_index + increment])

#                 elif isinstance(cur_val, list ) and  (ca_item[ca_item_index] in cur_val):
#                     next_val = sub_array_temp[ind_p1]
#                     if next_val == None:
#                         sub_array_temp[ind_p1] = ca_item[ca_item_index + increment]
#                     if isinstance(next_val, str):
#                         sub_array_temp[ind_p1] = [next_val , ca_item[ca_item_index + increment]]
#                     if isinstance(next_val, list):
#                         sub_array_temp[ind_p1].append(ca_item[ca_item_index + increment])
#                     new_form[the_index] = sub_array_temp
#                     tracking_dict.update( {ca_item[ca_item_index + increment] : the_index} )
#                     used_words_set.add(ca_item[ca_item_index + increment])

#         elif first_level_repetition_found and second_level_repetition_found:
#             print( "INTRESTING CASE : ", ca_item)
#             # YES THESE SHOULDNT BE ADDED















#         # for final_item in new_form:

#         #     # IF There is repetition in the same level
#         #     # FOR LOOP FOR CHECKING PREVIOUS LEVEL
#         #     for prv_levels in range( level , result_len + 1 ):

#         #         if ca_item[1] == final_item[ result_len - level ]:
#         #             repetition_found = True

#         #             index_of_newform = new_form.index(final_item)

#         #             temp_newform_subarray = new_form[index_of_newform]

#         #             next_position = temp_newform_subarray[ result_len - (prv_levels - 1)]
#         #             if ca_item[2] not in used_words_set:
#         #               if next_position == None:
#         #                   new_form[index_of_newform][result_len - (prv_levels - 1)] = ca_item[2]
#         #               elif isinstance(next_position,str):
#         #                   new_form[index_of_newform][result_len - (prv_levels- 1)] = [ next_position , ca_item[2]]
#         #               elif isinstance(next_position, list):
#         #                   new_form[index_of_newform][result_len - (prv_levels- 1)].append( ca_item[2])
#         #               used_words_set.add(ca_item[2])


#         # if not repetition_found:
#         #     #Else create new item
#         #     temp = [None] * (result_len + 1)
#         #     if ca_item[1] not in used_words_set:
#         #       temp[result_len - (level )] = ca_item[1]
#         #     if ca_item[2] not in used_words_set:
#         #       temp[result_len - (level - 1)] = ca_item[2]
#         #     new_form.append(temp)
#         #     used_words_set.add(ca_item[1])
#         #     used_words_set.add(ca_item[2])

# REMOVE THE NONES
# for i in range(len(new_form)):
#     new_sub_arr = []
#     for j in range(len(new_form[i])):

#         if new_form[i][j] == None:
#             continue
#         else:
#             new_sub_arr.append(new_form[i][j])

#     new_form[i] = new_sub_arr
# %%
# NEW FORM IS READY FOR PAGE BY PAGE SEARCH
def list_of_word_to_nested_words ( words : list):

    words.sort(key = lambda x: len(x) )
    print(words)

    nested_search_word , arrangement = listWord_to_dictWords(words)

    arrangement.sort( key = lambda x : x[0] , reverse = True)

    #BREAK

    print(arrangement)

    unique_groups =  list({ i[0] for i in arrangement  })
    unique_groups.sort( reverse=True)
    print(unique_groups)

    result = { i : [d for d in arrangement if d[0] == i] for i in unique_groups  }
    result_len = len(result)
    new_form = []

    arrays = [[]]*(result_len+1) ## Each Array From left to right is a column

    count = 1
    used_words_set = set()
    tracking_dict = {}

    for level in range( result_len , 0, -1):
        #print(i)

        current_array = result[level]
        lenOf_current_array = len(current_array)

        for ca_item in current_array:

            first_level_repetition_found = ca_item[1] in used_words_set
            second_level_repetition_found = ca_item[2] in used_words_set

            if not first_level_repetition_found and not second_level_repetition_found:
                #Create New Row
                #IF first level is not found, just add second level, whether its found or not
                temp = [None] * (result_len +1 )
                temp[ result_len - level ] = ca_item[1]
                temp[ result_len - (level - 1)] = ca_item[2]

                used_words_set.add(ca_item[1])
                used_words_set.add(ca_item[2])

                tracking_dict.update( { ca_item[1] : len(new_form) , ca_item[2] : len(new_form)} )

                new_form.append(temp)

            elif (first_level_repetition_found and not second_level_repetition_found) or (not first_level_repetition_found and second_level_repetition_found):
                #Find The Row
                the_index = -1
                increment = 0
                ca_item_index = 0
                ca_next_item_index = 0
                if(first_level_repetition_found and not second_level_repetition_found):
                    ca_item_index = 1
                    increment = 1
                else:
                    ca_item_index = 2
                    increment = -1
                the_index = tracking_dict[ca_item[ca_item_index]]
                sub_array_temp = new_form[the_index]

                for ind in range(len(sub_array_temp)):
                    cur_val = sub_array_temp[ind]
                    ind_p1 = ind + increment
                    if isinstance(cur_val, str) and cur_val == ca_item[ca_item_index]:
                        next_val = sub_array_temp[ind_p1]
                        if next_val == None:
                            sub_array_temp[ind_p1] = ca_item[ca_item_index + increment]
                        if isinstance(next_val, str):
                            sub_array_temp[ind_p1] = [next_val , ca_item[ca_item_index + increment]]
                        if isinstance(next_val, list):
                            sub_array_temp[ind_p1].append(ca_item[ca_item_index + increment])
                        new_form[the_index] = sub_array_temp
                        tracking_dict.update( {ca_item[ca_item_index + increment] : the_index} )
                        used_words_set.add(ca_item[ca_item_index + increment])

                    elif isinstance(cur_val, list ) and  (ca_item[ca_item_index] in cur_val):
                        next_val = sub_array_temp[ind_p1]
                        if next_val == None:
                            sub_array_temp[ind_p1] = ca_item[ca_item_index + increment]
                        if isinstance(next_val, str):
                            sub_array_temp[ind_p1] = [next_val , ca_item[ca_item_index + increment]]
                        if isinstance(next_val, list):
                            sub_array_temp[ind_p1].append(ca_item[ca_item_index + increment])
                        new_form[the_index] = sub_array_temp
                        tracking_dict.update( {ca_item[ca_item_index + increment] : the_index} )
                        used_words_set.add(ca_item[ca_item_index + increment])

            elif first_level_repetition_found and second_level_repetition_found:
                print( "INTRESTING CASE : ", ca_item)
                # YES THESE SHOULDNT BE ADDED

    # REMOVE THE NONES
    for i in range(len(new_form)):
        new_sub_arr = []
        for j in range(len(new_form[i])):

            if new_form[i][j] == None:
                continue
            else:
                new_sub_arr.append(new_form[i][j])

        new_form[i] = new_sub_arr

    remove_set = set()
    copy_word = words.copy()
    if len(new_form) > 0:
        for sdd in new_form :
            copy_word.append(sdd)
            if isinstance(sdd,list):
              for sdd_d in sdd:
                # try:
                #   remove_set.add( sdd_d)
                # except:
                #   print("ERROR: ", sdd_d, sdd)
                if isinstance(sdd_d, list):
                    [ remove_set.add(ekew) for ekew in sdd_d]
                else:
                    remove_set.add(sdd_d)
            elif isinstance(sdd,str):
              remove_set.add(sdd)

        [copy_word.remove(dls) for dls in remove_set if dls in copy_word]

    return copy_word, new_form


def list_of_words_from_groupedWordsJson( json_file_path : str):
    with open(json_file_path, "r", encoding="utf-8") as jsonfile:
        output = json.load(jsonfile)

    mykk = list()
    for words in output:
      print("WORDS : ", words)
      result = list_of_word_to_nested_words(words)
      for iok in result[0]:

          if isinstance(iok, list) :
              #inddd = words.index()
              iok.reverse()
      mykk.append(result[0])

    return mykk


# %%
bbb = [
    "Burkinabe",
    "Burundian",
    "clarification",
    "commitment",
    "confrontation",
    "Congolese",
    "cooperation",
    "diaspora",
    "disabilities",
    "disparities",
    "dispute",
    "disputeabilities",
    "Djibouti",
    "Egyptian",
    "Eritrean",
    "governance",
    "head of state",
    "headquarters",
    "hosted",
    "ideals",
    "inspired",
    "integrated",
    "Kenyan",
    "lack",
    "launched",
    "legitimate",
    "mobilisation",
    "observer status",
    "organ",
    "prosperous",
    "reconciled",
    "robust",
    "Rwandan",
    "Somali",
    "substantial",
    "Sudanese",
    "summit",
    "Tanzanian",
    "timeframe",
    "troops",
    "Ugandan",
    "visible"
  ]

list_of_word_to_nested_words ( bbb )

# %%
list_of_words_from_groupedWordsJson(r"C:\Users\Mubarak Salley\Documents\Accede\Tenacity-Book-11\src\automation\dictionary-scripts\words_grouped.json")
