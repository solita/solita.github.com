#!/usr/bin/env bb
(require '[clojure.string :as str]
         '[cheshire.core :as json])

(def author->posts
  (->> (java.io.File. "_posts")
       .listFiles
       (filter #(str/ends-with? (.getName %) ".md"))
       (mapcat (fn [f]
                 (let [contents (slurp f)
                       [_ title] (re-find #"(?im)^title: (.*)$" contents)
                       authors (-> (re-find #"(?im)^.*author: (.*)$" contents)
                                   second
                                   (str/split #", "))]
                   (for [author authors]
                     {:title title :author author :post (str "_posts/" (.getName f))}))))
       (group-by :author)
       (into {} (map (fn [[author posts]]
                       ;; sort by date (part of filename)
                       [author (reverse (sort-by :post posts))])))
       (sort-by (comp count second))
       reverse))

#_(->> author-counts
     (map (fn [[author count]] {:author author :count count}))
     clojure.pprint/print-table)

(spit "_data/authors.json" (json/generate-string author->posts))
;(println "total authors: " (count author-counts))
