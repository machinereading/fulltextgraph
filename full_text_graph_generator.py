from nltk import Tree

# from src import kbox_loader as kl
import rest_call as rc
import json


def get_all_leafs(node):
    result = []
    for n in node:
        if str(type(n)) == "<class 'nltk.tree.Tree'>":
            result.extend(get_all_leafs(n))
        else:
            result.append(n)
    return result


def node_in_list(target, nodes):
    for node in nodes:
        s_open = node["s_open"]
        s_close = node["s_close"]
        t_open = target["s_open"]
        t_close = target["s_close"]
        if s_open == t_open and s_close == t_close:
            return True, node["id"]
    return False, -1


def get_node_id(t_open, t_close, nodes):
    node_id_list = []
    temp_list = []
    is_in = False
    for node in nodes:
        s_open = node["s_open"]
        s_close = node["s_close"]
        if int(s_open) == int(t_open) and int(s_close) == int(t_close):
            node_id_list.append(node["id"])
            return node_id_list
        elif int(s_open) == int(t_open) and int(s_close) < int(t_close):
            node_id_list.append(node["id"])
            is_in = True
        elif is_in and int(s_close) == int(t_close):
            node_id_list.append(node["id"])
            # node_id_list.extend(temp_list)
            is_in = False
            return node_id_list
        elif is_in and int(s_open) > int(t_open) and int(s_close) < int(t_close):
            node_id_list.append(node["id"])
    return node_id_list


def get_node_list_from_id_list(id_list, nodes):
    node_list = []
    for id in id_list:
        for node in nodes:
            if int(id) == int(node["id"]):
                node_list.append(node)
    return node_list


def add_sem_to_nodes(id_list, nodes, sem):
    for id in id_list:
        for node in nodes:
            if int(id) == int(node["id"]):
                node["sem"] = sem
    return nodes


def add_sem_to_edges(head_list, tail_list, edges, frame_index, sem):
    for edge in edges:
        edge_head_list = edge["head"]
        edge_tail_list = edge["tail"]
        if head_list == edge_head_list and tail_list == edge_tail_list:
            edge["sem"] = frame_index + "." + sem
            return
        if head_list == edge_tail_list and tail_list == edge_head_list:
            edge["sem"] = frame_index + "." + sem
            edge["head"] = head_list
            edge["tail"] = tail_list
            return
        if set(head_list).issubset(set(edge_head_list)) and set(tail_list).issubset(set(edge_tail_list)):
            edge["sem"] = frame_index + "." + sem
            edge["head"] = head_list
            edge["tail"] = tail_list
            return
        if set(head_list).issubset(set(edge_tail_list)) and set(tail_list).issubset(set(edge_head_list)):
            edge["sem"] = frame_index + "." + sem
            edge["head"] = head_list
            edge["tail"] = tail_list
            return

    edge = {}
    edge["lex"] = "NIL"
    edge["sem"] = frame_index + "." + sem
    edge["pos"] = "NIL"
    edge["s_open"] = -1
    edge["s_close"] = -1
    edge["head"] = head_list
    edge["tail"] = tail_list
    edges.append(edge)





def get_full_text_graph(text, do_Frame, do_L2K):

    result_graph = {}

    ## SurfaceGraph
    print("======== Surface Graph =======")
    surface = rc.call_surface(text)
    # for triplet in surface:
    #     for triple in triplet:
    #         print(triple[0], triple[1], triple[2])

    nodes = []
    edges = []
    id = 0
    triples = surface["triples"]
    for triple in triples:

        head_list = []
        tail_list = []

        print(triple)
        # if triple["p"] is False:
        #     continue
        # else:
        p = Tree.fromstring(triple["p"])
        p_lex, p_pos, p_s_open, p_s_close = p[0].split("/")
        if p_lex == "Tense":
            continue
        else:
            s = Tree.fromstring(triple["s"])
            for idx, n in enumerate(s):

                leaf_list = []
                if str(type(n)) == "<class 'nltk.tree.Tree'>":
                    leaf_list = get_all_leafs(n)
                else:
                    leaf_list.append(n)

                for leaf in leaf_list:
                    node = {}
                    lex, pos, s_open, s_close = leaf.split("/")
                    node["id"] = id
                    node["lex"] = lex
                    node["sem"] = "NIL"
                    node["ont"] = "NIL"
                    node["pos"] = pos
                    node["s_open"] = s_open
                    node["s_close"] = s_close
                    exist, exist_id = node_in_list(node, nodes)
                    if exist:
                        head_list.append(exist_id)
                    else:
                        if idx == 0:
                            edge = {}
                            temp_list = []
                            temp_list.append(id)
                            edge["head"] = temp_list
                        else:
                            temp_list = []
                            temp_list.append(id)
                            edge["tail"] = temp_list
                            edge["sem"] = "NIL"
                            edge["lex"] = "NIL"
                            edge["pos"] = "NIL"
                            edge["s_open"] = -1
                            edge["s_close"] = -1
                            edges.append(edge)
                            edge = {}
                            temp_list = []
                            temp_list.append(id)
                            edge["head"] = temp_list
                        nodes.append(node)
                        head_list.append(id)
                        id = id + 1

            o = Tree.fromstring(triple["o"])
            enum = enumerate(o)
            for idx, n in enum:
                leaf_list = []
                if str(type(n)) == "<class 'nltk.tree.Tree'>":
                    leaf_list = get_all_leafs(n)
                else:
                    leaf_list.append(n)

                for leaf in leaf_list:
                    node = {}
                    lex, pos, s_open, s_close = leaf.split("/")
                    node["id"] = id
                    node["lex"] = lex
                    node["sem"] = "NIL"
                    node["ont"] = "NIL"
                    node["pos"] = pos
                    node["s_open"] = s_open
                    node["s_close"] = s_close
                    exist, exist_id = node_in_list(node, nodes)
                    if exist:
                        tail_list.append(exist_id)
                    else:
                        if idx == 0:
                            edge = {}
                            temp_list = []
                            temp_list.append(id)
                            edge["head"] = temp_list
                        else:
                            temp_list = []
                            temp_list.append(id)
                            edge["tail"] = temp_list
                            edge["sem"] = "NIL"
                            edge["lex"] = "NIL"
                            edge["pos"] = "NIL"
                            edge["s_open"] = -1
                            edge["s_close"] = -1
                            edges.append(edge)
                            edge = {}
                            temp_list = []
                            temp_list.append(id)
                            edge["head"] = temp_list
                        nodes.append(node)
                        tail_list.append(id)
                        id = id + 1


            edge = {}
            edge["lex"] = p_lex
            edge["sem"] = "NIL"
            edge["pos"] = p_pos
            edge["s_open"] = p_s_open
            edge["s_close"] = p_s_close
            edge["head"] = head_list
            edge["tail"] = tail_list
            edges.append(edge)

    ## FrameNet
    if do_Frame:
        print("======= FrameNet Graph =======")
        frames = rc.call_frame(text)
        for frame in frames:
            lu = frame["lu"]
            frame_index = frame["frame"]
            denotations = frame["denotations"]
            head_list = []
            for denotation in denotations:
                s_open = denotation["span"]["begin"]
                s_close = denotation["span"]["end"]
                role = denotation["role"] # TARGET or ARGUMENT
                obj = denotation["obj"]
                if role == "TARGET":
                    # add sem to vertex
                    head_list = get_node_id(s_open, s_close, nodes)
                    if len(head_list) > 0:
                        add_sem_to_nodes(head_list, nodes, obj)
                elif role == "ARGUMENT":
                    # add sem to edge
                    tail_list = get_node_id(s_open, s_close, nodes)
                    if len(tail_list) > 0:
                        add_sem_to_edges(head_list, tail_list, edges, frame_index, obj)

    result_graph["docID"] = 0
    result_graph["senID"] = 0
    result_graph["vertex"] = nodes
    result_graph["edge"] = edges

    #
    # ## L2K
    # entity_dict = {}
    # if do_L2K:
    #     print("======== L2K Triples =========")
    #     l2k = rc.call_l2k(text)
    #     EL = l2k["EL"]
    #     sentence = EL["sentence"][0]
    #     ELU = sentence["ELU"]
    #     entities = ELU["entities"]
    #
    #     for entity in entities:
    #         text = entity["text"]
    #         uri = entity["uri"].replace("http://kbox.kaist.ac.kr/resource/", "")
    #         entity_dict[text] = uri
    #
    #     print(entity_dict)
    #
    #     PL = l2k["PL"]
    #     triples = PL["triples"]
    #
    #     for triple in triples:
    #         print(triple["s"], triple["p"], triple["o"], triple["sco"])
    #     print("==============================")
    #     print()


    print(json.dumps(result_graph, ensure_ascii=False))

    return result_graph





# text = "한지운은 9회초 타석에 들어섰으나 송승준에게 사구를 맞았다."
# text = "게이츠는 2008년 6월 MS 이사회 의장에서 물러나 경영에서 손을 뗀 뒤 아내와 함께 세운 빌앤드멀린다게이츠 재단의 공동 이사장으로 일하면서 세계를 무대로 사회 공헌활동에 주력하고 있다."
# text = "국가보안위원회는 1954년부터 1991년까지 존속했던 소련의 정보 기관이다."
text = "근우회는 1927년에 조직된 한국의 여성 단체이다."
# text = "쿠바에서 몇년간 생활을 했고, 말년에는 피델 카스트로와도 알고 지내는 사이였기 때문에 관광업의 비중이 높아진 뒤의 쿠바에서는 허밍웨이를 체 게바라와 함께 관광상품으로 써먹고 있다."

get_full_text_graph(text, True, False)
