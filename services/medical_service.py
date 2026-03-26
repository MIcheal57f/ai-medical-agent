from core.rag import ask_medical_question
from core.rewrite import rewrite_query
from utils.logger import get_logger

logger = get_logger("service")

def medical_chat(question, history):

    logger.info("用户输入: %s", question)

    rewritten_question = rewrite_query(question, history)

    logger.info("用户输入: %s", question)

    answer, sources = ask_medical_question(
        rewritten_question,
        history
    )

    return answer, sources