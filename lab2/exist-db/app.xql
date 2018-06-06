xquery version "3.1";

module namespace app="http://exist-db.org/apps/wikipedia/templates";

import module namespace templates="http://exist-db.org/xquery/templates";
import module namespace config="http://exist-db.org/apps/wikipedia/config" at "config.xqm";

declare variable $app:uri := "http://localhost:8080/exist/apps/wikipedia";
declare variable $app:data_uri := "/db/apps/wikipedia/data";

declare function app:main($node as node(), $model as map(*)) {
    let $categories :=
        for $category in xmldb:get-child-collections($app:data_uri)
            return concat($app:data_uri, "/", $category)
    
    return map { "categories" := $categories }
};

declare function app:main-categories($node as node(), $model as map(*)) {
    for $category in $model("categories")
        let $name := <h3>{util:unescape-uri(replace(xs:anyURI($category), ".+/(.+)$", "$1"), "UTF-8")}</h3>
        
        let $pages :=
            for $page in xmldb:get-child-resources($category)
                return (
                    <li>
                        <a href="{concat($app:uri, "/page.html?pageid=", doc(concat($category, "/", $page))/page/pageid/text())}">
                            {doc(concat($category, "/", $page))/page/title/text()}
                        </a>
                    </li>
                )
        
        return ($name, $pages)
};

declare function app:page($node as node(), $model as map(*), $pageid as xs:int?) as map(*) {
    let $page :=
        for $p in collection(concat($app:data_uri, "//?select=*.xml"))
            where $p/page/pageid=$pageid
                return $p
    
    return map { "page" := $page }
};

declare function app:page-pageid($node as node(), $model as map(*)) as xs:string {
    $model("page")/page/pageid
};

declare function app:page-title($node as node(), $model as map(*)) as xs:string {
    $model("page")/page/title
};

declare function app:page-category($node as node(), $model as map(*)) as xs:string {
    $model("page")/page/category
};

declare function app:page-sections($node as node(), $model as map(*)) {
    for $section in $model("page")/page/sections/section
        return (
            <li>
                <h5>{data($section/@title)}</h5>
                <p>{$section/text()}</p>
            </li>
        )
};

declare %templates:default("q", "") function app:search($node as node(), $model as map(*), $q as xs:string?, $mode as xs:string?) {
    if($q = "") then (
        <div>Enter the query</div>
    ) else (
        let $starttime as xs:time := util:system-time()
        
        let $collection :=
            if($mode = "simple") then (
                collection(concat($app:data_uri, "//?select=*.xml"))/page/sections/section[contains(text(), $q)]
            ) else (
                collection(concat($app:data_uri, "//?select=*.xml"))/page/sections/section[ft:query(., $q)]
            )
        
        let $endtime as xs:time := util:system-time()
        
        let $results :=
            for $section in $collection
                return (
                    <div>
                        <h4>
                            <a href="{concat($app:uri, "/page.html?pageid=", root($section)//pageid/text())}">
                                {string(root($section)//title/text())}
                            </a>
                        </h4>
                        <p>{string($section/text())}</p>
                        <br/>
                    </div>
                )
        
        return (
           <div>
                <h3>Search phrase: "{$q}"</h3>
                <h3>Time: {seconds-from-duration($endtime - $starttime)}</h3>
                {$results}
            </div>
       )
    )
};

declare %templates:default("q", "") function app:analysis($node as node(), $model as map(*), $q as xs:string?) {
    if($q = "") then (
        <div>Enter the query</div>
    ) else (
        let $documents := collection(concat($app:data_uri, "/", $q, "/?select=*.xml"))
        let $sections := $documents//section
        let $all_words := ($sections ! tokenize(., "[\s]+"))
        let $words := distinct-values($all_words)
        
        let $results :=
            (for $word in $words
                let $amount := fn:count($all_words[. = $word])
                order by $amount descending
                
                return (
                    <tr>
                        <td>{string($word)}</td>
                        <td>{string($amount)}</td>
                    </tr>
                )
            )[position() = 1 to 100]
        
        return (
            <div>
                <p>Category: {$q}</p>
                <p>Total words: {count($all_words)}</p>
                <p>Total unique words: {count($words)}</p>
                <table border="1">
                    <tr>
                        <th>Word</th>
                        <th>Count</th>
                    </tr>
                    {$results}
                </table>
            </div>
        )
    )
};
