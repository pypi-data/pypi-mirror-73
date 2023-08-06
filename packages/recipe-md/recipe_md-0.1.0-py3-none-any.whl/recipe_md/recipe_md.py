from recipe_scrapers import scrape_me, WebsiteNotImplementedError
from slugify import slugify

from .utils import shrink_image


class Recipe:
    '''Scrape a recipe from `gousto.co.uk` and convert it to markdown
    To be extended to other websites in the near future.'''
    def __init__(self, name, host='gousto.co.uk'):
        self.host = host
        self.recipe = self.scrape_recipe(name)

    def scrape_recipe(self, name):
        slug = slugify(name)
        url = 'https://' + self.host + '/' + 'cookbook' + '/' + 'recipes'
        recipe = dict()
        try:
            scraped_recipe = scrape_me(url + '/' + slug)
            instructions = [i for i in scraped_recipe.instructions(
                ).split('\n')]
            recipe = {
                    'title': scraped_recipe.title(),
                    'image': scraped_recipe.image(),
                    'serves': scraped_recipe.yields(),
                    'time': scraped_recipe.total_time(),
                    'ingredients': scraped_recipe.ingredients(),
                    'instructions': instructions
                    }
        except WebsiteNotImplementedError:
            pass

        return recipe

    def make_md(self):
        image = shrink_image(self.recipe['image'], 'images')
        title = f"## {self.recipe['title']}"
        img = f"![Recipe picture](/images/{image})"
        time = f"Prep time: **{self.recipe['time']}** \
                [{self.recipe['serves']}]"
        ingr_t = '### Ingredients'
        ingr = "\n".join([f"- {i}" for i in self.recipe['ingredients']])
        instr_t = '### Instructions'
        instr = "\n".join([f"{num+1}. {item}"
                          for num, item in enumerate(
                              self.recipe['instructions'])])
        with open(self.recipe['title'].strip() + '.md', 'a') as f:
            for i in [title, img, time, ingr_t, ingr, instr_t, instr]:
                f.write(i + '\n\n')
