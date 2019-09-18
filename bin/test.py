from wordcloud import WordCloud

wordcloud = WordCloud()
wordcloud.generate_from_frequencies({'Hi': 2, 'Bye': 1})
# import matplotlib.pyplot as plt
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate_from_frequencies({'Hi': 2, 'Bye': 1})
wordcloud.to_file("wordcloud.png")

# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()
#
# # The pil way (if you don't have matplotlib)
# # image = wordcloud.to_image()
# # image.show()
