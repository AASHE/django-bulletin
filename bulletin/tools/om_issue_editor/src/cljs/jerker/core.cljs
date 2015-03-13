(ns jerker.core
  (:require [cljs.core.async :refer [<! put! chan]]
            [om.core :as om :include-macros true]
            [om.dom :as dom :include-macros true]
            [om-bootstrap.button :as b]
            [om-bootstrap.grid :as g]
            [om-bootstrap.panel :as p]
            [om-bootstrap.random :as r]
            [ajax.core :refer [DELETE GET]])
  (:require-macros [cljs.core.async.macros :refer [go]]))

(comment

  Jan. 30, 2015

  Status: pretty much blocked by lack of CORS headers from
  runserver.

  What to implement next:
  - remove posts
  - sort posts
  - edit posts
  - delete sections

  Feb. 1, 2015

  Status: CORS stuff was a red herring. Problem was DELETE was
  getting redirected because it didn't end in a slash. Pass DELETE
  to a URL with a slash on it and it works.

  The problem has not been addressed, yes, noted, thank *you*!
  )

(enable-console-print!)

(def api-url "http://127.0.0.1:8000/newsletter/api/")

(def edit-post-ch (chan))

(defn edit-post-button [post owner]
  (om/component
   (b/button {:bs-style "default"
              :onClick #(put! edit-post-ch (:id @post))}
             (r/glyphicon {:glyph "edit"}))))

(def move-post-ch (chan))

(defn move-post-up-button [post owner]
  (om/component
   (b/button {:bs-style "default"
              :onClick #(put! move-post-ch {:post-id (:id @post)
                                            :direction :up})}
             (r/glyphicon {:glyph "arrow-up"}))))

(defn move-post-down-button [post owner]
  (om/component
   (b/button {:bs-style "default"
              :onClick #(put! move-post-ch {:post-id (:id @post)
                                            :direction :down})}
             (r/glyphicon {:glyph "arrow-down"}))))

(def remove-post-ch (chan))

(defn remove-post-button [post owner]
  (om/component
   (b/button {:bs-style "default"
              :onClick #(put! remove-post-ch (:id @post))}
             (r/glyphicon {:glyph "remove"}))))

(defn post-row [post owner]
  (om/component
   (g/row nil
          (g/col {:xs 9 :md 6}
                 (:title post))
          (g/col {:xs 3 :className "pull-left"}
                 (om/build edit-post-button post)
                 (om/build move-post-up-button post)
                 (om/build move-post-down-button post)
                 (om/build remove-post-button post)))))

(defn post-grid [posts owner]
  (om/component
   (dom/div nil
          (apply g/grid nil
                 (map #(om/build post-row %) posts)))))

(defn oh-noes [error]
  (.log js/console "********************* wah ***********************)")
  (.log js/console "something bad happended: ")
  (.log js/console (str ":status " (:status error)))
  (.log js/console (str ":status-text " (:status-text error)))
  (.log js/console (str ":response " (:response error)))
  (.log js/console "********************* wah ***********************)"))

(defn edit-post [post-id]
  (.log js/console (str "edit-post: " post-id)))

(defn move-post [post-id direction]
  (.log js/console (str "move-post: " post-id " " direction)))

(defn remove-post-on-server [section-id post-id]
  (DELETE (str api-url "section/" section-id "/post/" post-id "/")
       {:handler #(.log js/console (str "remove-post:handler: " %))
        :error-handler oh-noes
        :format :json
        :response-format :json
        :keywords? true}))

(defn section-contains-post-id? [section post-id]
  ;; Does `section` contain a post with :id of `post-id`?
  (contains? (set (map :id (:posts section)))
             post-id))

(def remove-section-ch (chan))

(def add-post-ch (chan))

(defn section-row [section owner]
  (reify
    om/IWillMount
    (will-mount [_]
      (go (while true
            (let [post-id (<! edit-post-ch)]
              (edit-post post-id))))
      (go (while true
            (let [{:keys [post-id direction]} (<! move-post-ch)]
              (move-post post-id direction))))
      (go (while true
            (let [post-id (<! remove-post-ch)]
              (if (section-contains-post-id? @section post-id)
                (doseq []
                  (remove-post-on-server (:id @section) post-id)
                  (om/transact! section
                                :posts
                                (fn [posts]
                                  (vec (remove #(= post-id (:id %)) posts)))))
                ;; If not in this section, put post-id back on the bus
                ;; so the listeners in other sections can get it.
                (put! remove-post-ch post-id))))))
    om/IRender
    (render [_]
      (g/row nil
             (p/panel {:header (g/grid nil
                                       (g/row nil
                                              (g/col {:xs 9 :md 6}
                                                     (dom/h4 nil (:name section)))
                                              (g/col {:xs 3 :className "pull-left"}
                                                     (b/button {:bs-style "default"
                                                                :onClick #(put! remove-section-ch (:id @section))}
                                                               (r/glyphicon {:glyph "remove"}))
                                                     (b/button {:bs-style "default"
                                                                :onClick #(put! add-post-ch (:id @section))}
                                                               (r/glyphicon {:glyph "plus"})))))}
                      (om/build post-grid (:posts section)))))))

(defn delete-section-on-server [section-id]
  (.log js/console "delete-section-on-server stub called."))

(defn section-grid [sections owner]
  (reify
    om/IWillMount
    (will-mount [_]
      (go (while true
            (let [section-id (<! remove-section-ch)]
              (delete-section-on-server section-id)
              (om/update! sections (vec (filter #(not (= section-id (:id %))) @sections)))))))
    om/IRender
    (render [_]
      (dom/div nil
               (apply g/grid nil
                      (map #(om/build section-row %) sections))))))

(def issue-loaded-ch (chan))

(defn load-issue [id]
  (GET (str api-url "issue/" id "/")
       {:handler #(put! issue-loaded-ch %)
        :error-handler oh-noes
        :format :json
        :response-format :json
        :keywords? true}))

(defn load-available-posts []
  [{:id 6 :title "Pretty Good Post."}
   {:id 7 :title "Golden Yes *Golden* Opportunity."}
   {:id 8 :title "Most Popular Post."}])

(defn root [app-state owner]
  (reify
    om/IWillMount
    (will-mount [_]
      (go (while true
            (let [loaded-issue (<! issue-loaded-ch)]
              (om/update! app-state [:issue] loaded-issue))))
      (load-issue 279)
      (load-available-posts))
    om/IRender
    (render [_]
      (let [issue (:issue app-state)]
        (om/build section-grid (:sections issue))))))

(def app-state (atom {:issue {:sections []}
                      :available-posts []}))

(defn main []
  (om/root root
           app-state
           {:target (. js/document (getElementById "app"))}))

(comment
  ;; Attempts to address resorting vector.
  ;; Alternative approach is to store Post.position in
  ;; app-data, and update that when a Post is moved --
  ;; that should cause the list of Posts to be redrawn,
  ;; in the correct order, right?

  (defn move-element [element, vector, direction]
    (if (or (and (= direction :up)
                 (= element (first vector)))
            (and (= direction :up)
                 (= element (last vector))))
      vector)
    )

  (def m [1 2 3 4])

  (defn swap [m k1 k2]
    (assoc m k1 (get m k2) k2
           (get m k1))))
