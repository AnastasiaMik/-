<!-- news_template.tpl -->
<table border=1>
    <tr>
        <th>Title</th>
        <th>Author</th>
        <th colspan="1">Label</th>
    </tr>
    %for row in rows1:
        <tr>
            <td><a href="{{row.url}}">{{row.title}}</a></td>
            <td>{{row.author}}</td>
            <td>{{row.label}}</td>
        </tr>

    %end

    %for row in rows2:
        <tr>
            <td><a href="{{row.url}}">{{row.title}}</a></td>
            <td>{{row.author}}</td>
            <td>{{row.label}}</td>
        </tr>
     %end

    %for row in rows3:
        <tr>
            <td><a href="{{row.url}}">{{row.title}}</a></td>
            <td>{{row.author}}</td>
            <td>{{row.label}}</td>
        </tr>
    %end
</table>
