function add_question(type){
	var base_div=document.getElementById("ques_list");
	var new_question_div=document.createElement("div");
	var count=0;
	while(document.getElementById("ques_"+count+".div")!=null)count++;
	new_question_div.id="ques_"+count+".div";
	new_question_div.name="ques_"+count+".div";
	
	var new_question_type=document.createElement("input");
	new_question_type.id="ques_"+count+".type";
	new_question_type.name="ques_"+count+".type";
	new_question_type.type="Hidden";
	new_question_type.value=type;
	new_question_div.appendChild(new_question_type);

	var new_question_description=document.createElement("input");
	new_question_description.id="ques_"+count+".description";
	new_question_description.name="ques_"+count+".description";
	new_question_description.type="text";
	new_question_description.value="请输入题目描述";
	new_question_div.appendChild(new_question_description);

	var new_question_delete=document.createElement("input");
	new_question_delete.type="button";
	new_question_delete.value="删除该题目";
	new_question_delete.setAttribute("onclick","delete_question(this)");
	new_question_div.appendChild(new_question_delete);

	var new_question_up=document.createElement("input");
	new_question_up.type="button";
	new_question_up.value="上移";
	new_question_up.setAttribute("onclick","move_question(this,0)");
	new_question_div.appendChild(new_question_up);

	var new_question_down=document.createElement("input");
	new_question_down.type="button";
	new_question_down.value="下移";
	new_question_down.setAttribute("onclick","move_question(this,1)");
	new_question_div.appendChild(new_question_down);

	var new_option_ul=document.createElement("ul");
	new_question_div.appendChild(new_option_ul);

	if(type==0){
		new_option_ul.innerHTML="<li><input type=\"button\" value=\"添加选项\" onclick=\"add_option(this,0)\"/></li>"+
		"<li><input type=\"radio\"/><input type=\"text\" id=\"ques_"+
		count+".option_0\" name=\"ques_"+count+".option_0\" value=\"选项一\"/>"+
		"<input type=\"button\" value=\"删除\" onclick=\"delete_option(this)\"></li>"+
		"<li><input type=\"radio\"/><input type=\"text\" id=\"ques_"+
		count+".option_1\" name=\"ques_"+count+".option_1\" value=\"选项二\"/>"+
		"<input type=\"button\" value=\"删除\" onclick=\"delete_option(this)\"></li>";
	}
	else if(type==1){
		new_option_ul.innerHTML="<li><input type=\"button\" value=\"添加选项\" onclick=\"add_option(this,1)\"/></li>"+
		"<li><input type=\"checkbox\"/><input type=\"text\" id=\"ques_"+
		count+".option_0\" name=\"ques_"+count+".option_0\" value=\"选项一\"/>"+
		"<input type=\"button\" value=\"删除\" onclick=\"delete_option(this)\"></li>"+
		"<li><input type=\"checkbox\"/><input type=\"text\" id=\"ques_"+
		count+".option_1\" name=\"ques_"+count+".option_1\" value=\"选项二\"/>"+
		"<input type=\"button\" value=\"删除\" onclick=\"delete_option(this)\"></li>";
	}
	else if(type==2){
		new_option_ul.innerHTML="<li><input type=\"radio\"/><label>是</label></li>"+
		"<li><input type=\"radio\"/><label>否</label></li>";
	}
	else if(type==3){
		new_option_ul.innerHTML="<li><input type=\"text\" readonly=\"true\"/></li>";
	}

	base_div.appendChild(new_question_div);
}

function delete_question(obj){
	count=obj.parentNode.id[5];
	var current_question=document.getElementById("ques_"+count+".div");
	current_question.parentNode.removeChild(current_question);
	count++;
	current_question=document.getElementById("ques_"+count+".div");
	while(current_question!=null){
		var question_div=document.getElementById("ques_"+count+".div");
		question_div.id="ques_"+(count-1)+".div";
		question_div.name="ques_"+(count-1)+".div";

		var question_type=document.getElementById("ques_"+count+".type");
		question_type.id="ques_"+(count-1)+".type";
		question_type.name="ques_"+(count-1)+".type";
		var type=question_type.value;

		var question_description=document.getElementById("ques_"+count+".description");
		question_description.id="ques_"+(count-1)+".description";
		question_description.name="ques_"+(count-1)+".description";


		if(type<2){
			var option_count=0;
			var current_option=document.getElementById("ques_"+count+".option_"+option_count);
			while(current_option!=null){
				current_option.id="ques_"+(count-1)+".option_"+option_count;
				current_option.name="ques_"+(count-1)+".option_"+option_count;
				option_count++;
				current_option=document.getElementById("ques_"+count+".option_"+option_count);
			}
		}

		count++;
		current_question=document.getElementById("ques_"+count+".div");
	}
}

function move_question(obj,direction){
	var count=obj.parentNode.id[5];
	var next_count=count;
	if(direction==1){
		next_count++;
	}
	else{
		next_count--;
	} 

	var current_question_div=document.getElementById("ques_"+count+".div");
	var next_question_div=document.getElementById("ques_"+next_count+".div");

	if(current_question_div==null||next_question_div==null)return;

	current_question_div.id="ques_"+next_count+".div";
	current_question_div.name="ques_"+next_count+".div";
	next_question_div.id="ques_"+count+".div";
	next_question_div.name="ques_"+count+".div";

	var current_question_type=document.getElementById("ques_"+count+".type");
	var next_question_type=document.getElementById("ques_"+next_count+".type");
	current_question_type.id="ques_"+next_count+".type";
	current_question_type.name="ques_"+next_count+".type";
	next_question_type.id="ques_"+count+".type";
	next_question_type.name="ques_"+count+".type";

	var current_type=current_question_type.value;
	var next_type=next_question_type.value;
	
	var current_question_description=document.getElementById("ques_"+count+".description");
	var next_question_description=document.getElementById("ques_"+next_count+".description");
	current_question_description.id="ques_"+next_count+".description";
	current_question_description.name="ques_"+next_count+".description";
	next_question_description.id="ques_"+count+".description";
	next_question_description.name="ques_"+count+".description";

	if(current_type<2){
		if(next_type<2){
			var option_count=0;
			var current_option=document.getElementById("ques_"+count+".option_"+option_count);
			var next_option=document.getElementById("ques_"+next_count+".option_"+option_count);
			while(current_option!=null&&next_option!=null){
				current_option.id="ques_"+next_count+".option_"+option_count;
				current_option.name="ques_"+next_count+".option_"+option_count;
				next_option.id="ques_"+count+".option_"+option_count;
				next_option.name="ques_"+count+".option_"+option_count;
				option_count++;
				current_option=document.getElementById("ques_"+count+".option_"+option_count);
				next_option=document.getElementById("ques_"+next_count+".option_"+option_count);
			}
			while(current_option!=null){
				current_option.id="ques_"+next_count+".option_"+option_count;
				current_option.name="ques_"+next_count+".option_"+option_count;
				option_count++;
				current_option=document.getElementById("ques_"+count+".option_"+option_count);
			}
			while(next_option!=null){
				next_option.id="ques_"+count+".option_"+option_count;
				next_option.name="ques_"+count+".option_"+option_count;
				option_count++;
				next_option=document.getElementById("ques_"+next_count+".option_"+option_count);
			}
		}
		else while(current_option!=null){
				current_option.id="ques_"+next_count+".option_"+option_count;
				current_option.name="ques_"+next_count+".option_"+option_count;
				option_count++;
				current_option=document.getElementById("ques_"+count+".option_"+option_count);
			}		
	}
	else if(next_type<2){
		while(next_option!=null){
				next_option.id="ques_"+count+".option_"+option_count;
				next_option.name="ques_"+count+".option_"+option_count;
				option_count++;
				next_option=document.getElementById("ques_"+next_count+".option_"+option_count);
			}
	}
}

function add_option(obj,type){
	var ul=obj.parentNode.parentNode;
	var count=ul.parentNode.id[5];
	var ocount=0;
	var radio;
	if(type==0)radio="radio";
	else radio="checkbox";
	while(document.getElementById("ques_"+count+".option_"+ocount)!=null)ocount++;
	ul.innerHTML+="<li><input type=\""+radio+"\"/><input type=\"text\" id=\"ques_"+
		count+".option_"+ocount+"\" name=\"ques_"+count+".option_"+ocount+"\" value=\"选项一\"/>"+
		"<input type=\"button\" value=\"删除\" onclick=\"delete_option(this)\"></li>";
}

function delete_option(obj){
	var li=obj.parentNode;
	var ul=li.parentNode;
	var option=$(obj).prev();
	var ques_count=option.attr("id")[5];
	var option_count=option.attr("id")[14];
	ul.removeChild(li);

	option_count++;
	var current_option=document.getElementById("ques_"+ques_count+".option_"+option_count);
	while(current_option!=null){
		current_option.id="ques_"+ques_count+".option_"+(option_count-1);
		current_option.name="ques_"+ques_count+".option_"+(option_count-1);
		option_count++;
		current_option=document.getElementById("ques_"+ques_count+".option_"+option_count);
	}

}