#!/usr/bin/env bb
(require '[clojure.string :as str]
         '[clojure.data.json :as json])

(def author->posts
  (->> (java.io.File. "_posts")
       .listFiles
       (filter #(str/ends-with? (.getName %) ".md"))
       (mapcat (fn [f]
                 (for [author (-> (re-find #"(?im)^.*author: (.*)$" (slurp f))
                                  second
                                  (str/split #", "))]
                   {:author author :post f})))
       (group-by :author)
       (into {} (map (fn [[author posts]]
                       [author (map #(str "_posts/" (.getName (:post %))) posts)])))
       (sort-by (comp count second))
       reverse))

#_(->> author-counts
     (map (fn [[author count]] {:author author :count count}))
     clojure.pprint/print-table)

(spit "_data/authors.json" (json/write-str author->posts))
;(println "total authors: " (count author-counts))
