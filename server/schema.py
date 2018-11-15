from graphene import ObjectType, String, Schema


class Query(ObjectType):
    hello = String(argument=String(default_value="stranger"))

    def resolve_hello(self, info, argument):
        return 'Hello' + argument


schema = Schema(query=Query)
