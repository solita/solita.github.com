# Based on tag cloud script by Anurag Priyam: https://gist.github.com/yeban/2290195 (MIT license)

module Jekyll
  class TagCloud < Liquid::Tag
    safe = true

    attr_reader :size_min, :size_max, :precision, :unit, :threshold

    def initialize(name, params, tokens)
      # initialize default values
      @size_min, @size_max, @precision, @unit = 80, 170, 0, '%'
      @threshold                              = 1

      # process parameters
      @params = Hash[*params.split(/(?:: *)|(?:, *)/)]
      process_font_size(@params['font-size'])
      process_threshold(@params['threshold'])

      super
    end

    def render(context)
      hue, saturation, def_lightness = 207, 85, 43

      # get an Array of [tag name, tag count] pairs
      count = context.registers[:site].tags.map do |name, posts|
        [name, posts.count] if posts.count >= threshold
      end

      # clear nils if any
      count.compact!

      # get the minimum, and maximum tag count
      min, max = count.map(&:last).minmax

      # map: [[tag name, tag count]] -> [[tag name, tag weight]]
      weight = count.map do |name, count|
        # logarithmic distribution
        weight = (Math.log(count) - Math.log(min))/(Math.log(max) - Math.log(min))
        [name, weight]
      end

      # shuffle the [tag name, tag weight] pairs
      weight = weight.sort_by{|tag,html| tag.downcase}

      # reduce the Array of [tag name, tag weight] pairs to HTML
      weight.reduce("") do |html, tag|
        name, weight = tag
        size = size_min + ((size_max - size_min) * weight).to_f
        lightness = def_lightness - ((size - size_min) / 8)
        size = sprintf("%.#{@precision}f", size)
        html << %(<a class='tag'
          style='font-size: #{size}#{unit};
          color: hsl(#{hue}, #{saturation}%, #{lightness}%);' 
          href='/tag/#{name.gsub(/\W/, '-')}'>#{name.gsub(/\-/, ' ')}</a>\n)
      end
    end

    private

    def process_font_size(param)
      /(\d*\.{0,1}(\d*)) *- *(\d*\.{0,1}(\d*)) *(%|em|px)/.match(param) do |m|
        @size_min  = m[1].to_f
        @size_max  = m[3].to_f
        @precision = [m[2].size, m[4].size].max
        @unit      = m[5]
      end
    end

    def process_threshold(param)
      /\d*/.match(param) do |m|
        @threshold = m[0].to_i
      end
    end
  end
end

Liquid::Template.register_tag('tag_cloud', Jekyll::TagCloud)