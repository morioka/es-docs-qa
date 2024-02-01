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
from langchain.chains import VectorDBQAWithSourcesChain
from langchain.agents import AgentType, Tool

def chat(message: str) -> str:
    llm = setting.get_llm()
    qa = VectorDBQAWithSourcesChain.from_chain_type(llm, chain_type="map_reduce", vectorstore=setting.get_vector_store())

    tools = [
        Tool(
            name="elasticsearch_searcher",
            func=qa,
            description="useful for when you need to answer questions about the most recent elasticsearch knowledge."
        )
    ]

    agent = agents.initialize_agent(tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    question = _get_question_prompt(message)
    answer = agent.run(question)
    return answer

