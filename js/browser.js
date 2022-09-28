class BrowserUtils
{
  constructor()
  {
    this.checkattributes = ({element, attrib}) =>
    {
      this.element_defaults = {'css':{}, 'style':{}}
      if(attrib === 'text')
      {
        {
          if(element.innerText !== undefined && element.innerText !== '')
          {
            return element.innerText
          }
          else if(element.getAttribute('text') !== null && element.getAttribute('text') !== '')
          {
            return element.getAttribute('text')
          }
          else
          {
            return ''
          }
        }
      }
      else if (attrib === 'innerHTML' && element.innerHTML !== undefined)
      {
        return element.innerHTML
      }
      else if (attrib === 'style')
      {
        return this.buildDictKV({arr:element.getAttribute(attrib).split(";"),delim:':'})
      }
      else
      {
        return element.getAttribute(attrib) 
      }

    };
    this.buildAttribDict = ({element}) =>
    {
      let result_dict = {}
      let prop_names = element.getAttributeNames().toString().split(",");
      for(let att = 0; att < prop_names.length; att++)
      {
        if(prop_names[att] === '' || prop_names[att] === null)
        {
          continue
        };
        result_dict[prop_names[att]] = this.checkattributes({element:element,attrib:prop_names[att]})
      }
      return result_dict
    }
    this.buildDictBool = ({arr}) => 
    {
      let bool_dict = {}
      for(let i = 0; i < arr.length; i++)
      {
        if(arr[i] === "")
        {
          continue
        }
        bool_dict[arr[i]] = true
      }
      return bool_dict
    }

    this.buildDictKV = ({arr, delim = null}) =>
    {
      let key, value
      let kv_dict = {}
      for(let i = 0; i < arr.length; i++)
      {
        if(delim !== null)
        {
          let split_data = arr[i].split(delim)
          key = split_data[0]
          value = split_data[1]
        }
        
        if(key && value)
        {
          kv_dict[key] = value
        }
        else
        {
          kv_dict[arr[i]] = true
        }
      }
      return kv_dict
    }
    this.pullKeyfromDict = ({dict, key}) =>
    {
      if(dict[key] !== undefined)
      {
        return dict[key]
      }
      if(key in this.element_defaults)
      {
        return this.element_defaults[key]
      }
      return ''
    }
    this.removeTags = (tag) =>
    {
      let tags = document.querySelectorAll(tag);
      for (let i = 0; i < tags.length; i++) 
      {
          tags[i].remove();
      }
    }
    this.removeiFrames = () =>
    {
      let iframes = document.querySelectorAll('iframe');
      for (let i = 0; i < iframes.length; i++) 
      {
          if (navigator.appName == 'Microsoft Internet Explorer') 
          {
              window.frames[i].document.execCommand('Stop');
          } 
          else 
          {
              try
              {
                  window.frames[i].stop()
              }
              catch
              {
                  console.log('Removed within algorithm')
              }
              
          }
          iframes[i].remove();
      }
    }
  }

}

export class Selenium extends BrowserUtils
{
  constructor({txt_trgt = null, props_trgts = ['text','aria-label'], tags_trgts = ['DIV','A','SPAN'], action = 'match', xpath = null, element = null})
  {
    console.log('Constructor of Element ----------------------', element)
    super();
    this.props_trgts = props_trgts;
    this.txt_trgt = txt_trgt;
    this.action = action;
    this.xpath = xpath;
    this.tags_trgts = tags_trgts;
    this.element = element;
    this.ignore_tags = {'BR':true,'HR':true,'SPACER':true}
    this.HTML_MAPPING = {}
    this.MATCH = [];
    this.EL_BY_XPATH= null;
    this.EL_BY_EL = null;

    this.processAction = ({selector}) =>
    {
      if(this.action === 'match')
      {
        this.removeiFrames();
        this.HTML_MAPPING = this.buildElementGrid({element: document.querySelector(selector)})
        console.log(this.MATCH)
        return this.MATCH
      }
      if(this.action === 'grid')
      {
        this.removeiFrames();
        this.HTML_MAPPING = this.buildElementGrid({element: document.querySelector(selector)})
        console.log(this.HTML_MAPPING)
        return this.HTML_MAPPING
      }
      if(this.action === 'xpath')
      {
        this.removeiFrames();
        this.HTML_MAPPING = this.buildElementGrid({element: document.querySelector(selector)});
        console.log(this.EL_BY_XPATH)
        return this.EL_BY_XPATH
      }
      if(this.action === 'element')
      {
        this.removeiFrames();
        this.HTML_MAPPING = this.buildElementGrid({element: document.querySelector(selector)});
        return this.EL_BY_EL
      }
      return alert('Requested Process does not exist. Please choose Match or Grid.')

    }

    this.buildElementGrid = ({element, grid_id = [0], c_id = null, n = 0}) =>
    {
      this.removeiFrames()
      let match_vals = {};
      match_vals['css'] = this.buildDictBool({arr:element.className.toString().split(/\s+/)})
      match_vals['text'] = this.checkattributes({element: element,attrib:'text'})
      match_vals['properties'] = this.buildAttribDict({element:element})
      match_vals['scripts'] = this.pullKeyfromDict({dict: match_vals['properties'], key:'onclick'})
      match_vals['style'] = this.pullKeyfromDict({dict: match_vals['properties'],key:'style'})
      match_vals['type'] = 'element';
      match_vals['api_type'] = '';
      grid_id  =[...grid_id];
      if(c_id !== null){grid_id.push(c_id)};
      match_vals['TYG'] = grid_id;
      //element.setAttribute('TY_GRID',JSON.stringify(grid_id))
      if(this.txt_trgt !== null && this.props_trgts.length > 0 && this.action === 'match')
      {
        for(let prop = 0; prop < this.props_trgts.length; prop++)
        {
          if (this.txt_trgt.toUpperCase() === this.checkattributes({element: element, attrib: this.props_trgts[prop]}).toUpperCase())
          {
            console.log(this.txt_trgt)
            this.MATCH.push({"element":element,"xpath":grid_id})
          }
        }
      }
      let id_index
      if(this.action === 'xpath' && n + 1 < this.xpath.length)
      {
        id_index = this.xpath[n + 1] 
      }
      n = n + 1

      if(JSON.stringify(grid_id) === JSON.stringify(this.xpath) && this.action === 'xpath')
      {
        this.EL_BY_XPATH = {'element':element,'xpath':grid_id,'par_innerHTML':element.parentNode.innerHTML,'outerHTML':element.outerHTML}
      }

      //console.log('\nITERATION--------------------',element, this.element,'\n')
      if(element === this.element && this.action === 'element')
      {
        this.EL_BY_EL = {'element':element,'xpath':grid_id, 'par_innerHTML':element.parentNode.innerHTML,'outerHTML':element.outerHTML}
      }
      this.removeiFrames()
      let children = element.children;
      for(let i = 0; i < children.length; i++)
      {
        if(this.action === 'xpath')
        {
          if (id_index !== i)
          {
            //console.log([...grid_id,i], '------------------- Skipped')
            continue
          }
        }
        //console.log([...grid_id,i], '------------------- Not Skipped')
        match_vals[i] = this.buildElementGrid({element:children[i],grid_id:grid_id,c_id:i, n: n})
      }
      return match_vals
    }
  }
};
