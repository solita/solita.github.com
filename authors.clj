#!/usr/bin/env bb
(require '[clojure.string :as str]
         '[cheshire.core :as json]
         '[clj-yaml.core :as yaml])

(defn file->relative-url
  "Convert file like:
  _posts/1984-04-21-war-with-eurasia.md

to a jekyll page link:
  /1984/04/21/war-with-eurasia.html"
  [f]
  (apply format "/%s/%s/%s/%s.html"
         (drop 1 (re-find #"^(\d+)-(\d+)-(\d+)-(.*).md$" (.getName f)))))

(def author-by-handle
  (let [authors (-> "_config.yml" slurp yaml/parse-string :authors)]
    (fn [author-name]
      (authors (keyword author-name)))))

(defn yaml-header [post-file]
  (->> post-file slurp str/split-lines
       (drop 1)
       (take-while #(not= "---" %))
       (str/join "\n")
       yaml/parse-string))

(def author->posts
  (->> (java.io.File. "_posts")
       .listFiles
       (filter #(str/ends-with? (.getName %) ".md"))
       (mapcat (fn [f]
                 (let [{:keys [title author]} (yaml-header f)
                       authors (map str/trim (str/split author #","))]
                   (for [author authors]
                     {:title title :author author :url (file->relative-url f)}))))
       (group-by :author)
       (map (fn [[author posts]]
              ;; sort by date (part of filename)
              (assoc (author-by-handle author)
                     :handle author
                     :posts (->> posts
                                 (map #(dissoc % :author))
                                 (sort-by :url)
                                 reverse))))
       (sort-by (comp count :posts))
       reverse))

(spit "_data/authors.json" (json/generate-string author->posts))
