# Korean Full-text Graph

## About
Korean Full-text Graph (SurfaceGraph + FrameNet)

## Introduction
Full-text Graph란, 입력 문장 내용 전체를 하나의 그래프로 만들기 위한 목적의 프로젝트입니다. 이 코드는 한국어 Full-text graph를 생성하는 코드입니다. 현재 한국어 Full-text Graph는 [SurfaceGraph](https://github.com/sanghanam/SRDF)와 [FrameNet](https://github.com/machinereading/frameBERT) 파싱 결과를 활용해 두 그래프를 결합하는 방식으로 구현됩니다.

## How to use
Use ``full_service.py``

### How to run
Chunking: we use REGEX in [NLTK](https://www.nltk.org/), and [ETRI OPEN API POS tagger](https://aiopen.etri.re.kr/); see ``chunking.py``
SurfaceGraph parser: ``surface_graph_parser.py``
Frame parser: see ``rest_call.py - def call_frame(text)``

## Data Example
### SurfaceGraph Parser
Input: 
```
그는 코로나 바이러스의 항체를 만들었다.
```
<br>
Output:
```
(NP 그/NP/0/1) (J 는/JX/1/2) (VP 만들/VV/17/19 었/EP/19/20)
(VP 만들/VV/17/19 었/EP/19/20) (J 를/JKO/15/16) (NP 코로나_바이러스/NNP/3/11 의/JKG/11/12 항체/NNG/13/15)
(VP 만들/VV/17/19 었/EP/19/20) (T Tense/X/X/X) (E 다/EF/20/21 ./SF/21/22)
```
### [FrameNet Parser](https://github.com/machinereading/frameBERT)
### Full-text Graph
Input: 
```
그는 코로나 바이러스의 항체를 만들었다.
```
<br>

Output:
```
{
    "docID": 0,
    "edge": [
        {
            "head": [
                1
            ],
            "lex": "NIL",
            "pos": "NIL",
            "s_close": -1,
            "s_open": -1,
            "sem": "NIL",
            "tail": [
                2
            ]
        },
        {
            "head": [
                1,
                2
            ],
            "lex": "는",
            "pos": "JX",
            "s_close": "2",
            "s_open": "1",
            "sem": "Building.Agent",
            "tail": [
                0
            ]
        },
        {
            "head": [
                3
            ],
            "lex": "NIL",
            "pos": "NIL",
            "s_close": -1,
            "s_open": -1,
            "sem": "NIL",
            "tail": [
                4
            ]
        },
        {
            "head": [
                4
            ],
            "lex": "NIL",
            "pos": "NIL",
            "s_close": -1,
            "s_open": -1,
            "sem": "NIL",
            "tail": [
                5
            ]
        },
        {
            "head": [
                1,
                2
            ],
            "lex": "를",
            "pos": "JKO",
            "s_close": "16",
            "s_open": "15",
            "sem": "Building.Created_entity",
            "tail": [
                3,
                4,
                5
            ]
        }
    ],
    "senID": 0,
    "vertex": [
        {
            "id": 0,
            "lex": "그",
            "ont": "NIL",
            "pos": "NP",
            "s_close": "1",
            "s_open": "0",
            "sem": "NIL"
        },
        {
            "id": 1,
            "lex": "만들",
            "ont": "NIL",
            "pos": "VV",
            "s_close": "19",
            "s_open": "17",
            "sem": "Building"
        },
        {
            "id": 2,
            "lex": "었",
            "ont": "NIL",
            "pos": "EP",
            "s_close": "20",
            "s_open": "19",
            "sem": "Building"
        },
        {
            "id": 3,
            "lex": "코로나_바이러스",
            "ont": "NIL",
            "pos": "NNP",
            "s_close": "11",
            "s_open": "3",
            "sem": "NIL"
        },
        {
            "id": 4,
            "lex": "의",
            "ont": "NIL",
            "pos": "JKG",
            "s_close": "12",
            "s_open": "11",
            "sem": "NIL"
        },
        {
            "id": 5,
            "lex": "항체",
            "ont": "NIL",
            "pos": "NNG",
            "s_close": "15",
            "s_open": "13",
            "sem": "NIL"
        }
    ]
}
```


## Licenses
* `CC BY-NC-SA` [Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/2.0/)
* If you want to commercialize this resource, [please contact to us](http://mrlab.kaist.ac.kr/contact)

## Publisher
[Machine Reading Lab](http://mrlab.kaist.ac.kr/) @ KAIST

## Acknowledgement
This work was supported by Institute for Information & communications Technology Promotion(IITP) grant funded by the Korea government(MSIT) (2013-0-00109, WiseKB: Big data based self-evolving knowledge base and reasoning platform)
