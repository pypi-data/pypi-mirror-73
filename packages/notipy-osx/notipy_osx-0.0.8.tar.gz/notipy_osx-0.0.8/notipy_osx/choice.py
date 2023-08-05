import os
import subprocess


def quotify(string):
  return f'"{string}"'


# def choice_prompt(text="Please make your selection", choices, default_choice):
def choice_prompt(choices, default_choices, text="Please make your selection"):
  as_choices = '{%s}' % ', '.join(map(quotify, choices))
  as_default_choices = '{%s}' % ', '.join(map(quotify, default_choices))

  applescript = f'''\
  choose from list {as_choices} with prompt "{text}" default items {as_default_choices}
  '''.replace("'", '"')

  command = f"""
    osascript -e '\
      set answer to {applescript} 
      return answer
    '
  """

  try:
    # run the terminal command and get the output
    result = subprocess.check_output(command, shell=True)
    result_string = result.decode('utf-8').rstrip()
  except:
    # if there's an error, it means that the user has clicked on Cancel or or the escape key
    result_string = None

  if result_string == 'false':
    return None
  return result_string

