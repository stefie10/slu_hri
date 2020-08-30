import follow
import meet
import bring
import avoid
import wander
import go

verbs = [follow.Engine(),
         meet.Engine(),
         avoid.Engine(),
         bring.Engine(),
         wander.Engine(),
         go.Engine(),
         ]

verbMap = dict([(e.name, e) for e in verbs])
