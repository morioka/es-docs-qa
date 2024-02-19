import setting

from langchain.prompts import PromptTemplate


def _get_question_prompt(text: str) -> str:
    translate_template = """
        下記の質問に日本語で答えてください。また、参照元についても教えて下さい。
        質問：{question}
        回答：
        """
    prompt = PromptTemplate(
        input_variables=["question"],
        template=translate_template,
    )

    return prompt.format(question=text)


from langchain import agents
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain import hub

def chat(message: str) -> str:
    document_content_description="Elasticsearch documents"
    metadata_field_info=[]
    prompt = hub.pull("hwchase17/react")

    llm = setting.get_llm()
    retriever = SelfQueryRetriever.from_llm(
        llm, setting.get_vector_store(), document_content_description, metadata_field_info, verbose=True
    )    
    qa = RetrievalQAWithSourcesChain.from_chain_type(llm, chain_type="stuff", retriever=retriever)

    tools = [
        Tool(
            name="elasticsearch_searcher",
            func=qa,
            description="useful for when you need to answer questions about the most recent elasticsearch knowledge."
        )
    ]

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    question = _get_question_prompt(message)
    answer = agent_executor.invoke({"input": question})['output']
    return answer

