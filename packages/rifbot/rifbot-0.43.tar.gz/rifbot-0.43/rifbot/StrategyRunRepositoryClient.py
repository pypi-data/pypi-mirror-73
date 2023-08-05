from rifbot import GqlClient, RifbotClient
from rifbot.gql_queries import QUERIES, SUBSCRIPTIONS, MUTATIONS
from shortid import ShortId


class StrategyRunRepositoryClient:
    def __init__(self, service: GqlClient, root: RifbotClient):
        # print('StrategyRunRepositoryClient')
        self.root = root
        self.service = service

    async def findOneStrategyRunResult(self, runId:str):
        # print('findOneStrategyRunResult', 'runId:', runId)

        res = await self.service.query(QUERIES['FIND_ONE_STRATEGY_RUN_RESULT'], {
            'runId': runId
        })

        return res

    async def close(self):
        self.service.close()
        self.service.listen_coro.cancelled()
