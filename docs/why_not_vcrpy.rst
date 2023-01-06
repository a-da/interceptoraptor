Python vcr cassete
https://vcrpy.readthedocs.io/en/latest/

It just do not work for us:

1. The log is to big
    Its log too much or nothing, there is not truncate the logs.

2. Multi-threading/parallel
    Just does not work. In "interceptorator" we make sure about this by storing into threadsafe storage env 'sqlite'.

3. A blotted yaml dump
    It takes time to load entire yaml if is too big. There is no option to extract just one item.

4. Random params
    Http can send request params in random order, this is not handled or sorted before capture.

5. Environment/config is not taking into consideration
    OS env is an important things that also have to captured if we want to replay 1:1.
