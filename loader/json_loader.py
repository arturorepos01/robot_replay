import json

from models.action import Action


class JsonLoader:

    def load(self, archivo):

        with open(archivo, encoding="utf8") as f:

            datos = json.load(f)

        acciones = []

        for item in datos:

            acciones.append(

                Action(

                    flow_id=item.get("flow_id"),

                    tipo=item.get("tipo"),

                    tipo_logico=item.get("tipo_logico"),

                    tipo_componente=item.get("tipo_componente"),

                    modo=item.get("modo"),

                    tag=item.get("tag"),

                    texto=item.get("texto"),

                    valor=item.get("valor"),

                    field=item.get("field"),

                    placeholder=item.get("placeholder"),

                    id=item.get("id"),

                    name=item.get("name"),

                    clase=item.get("clase"),

                    url=item.get("url"),

                    timestamp=item.get("timestamp"),

                    container_tag=item.get("container_tag"),

                    container_class=item.get("container_class"),

                    index=item.get("index",0)

                )

            )

        return acciones