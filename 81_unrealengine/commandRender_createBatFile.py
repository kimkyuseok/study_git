import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import unreal
import re
def print_selected_items():
    # 파일 저장 경로 선택
    filename = filedialog.asksaveasfilename(initialdir="X:", title="Save BAT File", filetypes=[("Batch File", "*.bat")])
    # 선택된 경로가 없으면 종료
    if not filename:
        return
    # 선택된 경로에 .bat 확장자가 없는 경우 추가
    if not filename.endswith(".bat"):
        filename += ".bat"    
    # ... (파일 내용 쓰기 코드)
    returnString="@echo off\n"
    returnString=returnString + "\"C:\\Program Files\\Epic Games\\UE_5.3\\Engine\\Binaries\\Win64\\UnrealEditor-Cmd.exe\" "
    dpath=unreal.SystemLibrary.get_project_directory ( )
    fname=unreal.SystemLibrary.get_game_name ( )
    returnString=returnString+dpath+fname+'.uproject'
    # 각 셀렉트 박스에서 선택된 항목을 출력합니다.
    selected_movie_pipeline_config = movie_pipeline_primary_config_combobox.get()
    selected_level_sequence = level_sequence_combobox.get()
    selected_world = world_combobox.get()
    returnString=returnString+' '+selected_world+' -game -LevelSequence=\"'
    returnString=returnString+selected_level_sequence.replace('LevelSequence ','')+'\" -MoviePipelineConfig=\"'
    returnString=returnString+selected_movie_pipeline_config.replace('MoviePipelinePrimaryConfig ','')+'\" -windowed -Log -StdOut -allowStdOutLogVerbosity -Unattended'
    # 파일 저장
    with open(filename, "w") as f:
        # ... (파일 내용)
        f.write(returnString)

    
    # 저장 완료 메시지 출력
    tk.messagebox.showinfo("저장 완료", f"파일이 저장되었습니다: {filename}")
    window.destroy()
MPPC_list=[]
LS_list=[]
WD_list=[]
# 모든 에셋을 찾습니다.
all_assets = unreal.EditorAssetLibrary.list_assets('/Game', True, False)
for i in all_assets:
    renderAsset = unreal.load_asset(i)
    if renderAsset:
        if renderAsset.get_class().get_name() in ['MoviePipelinePrimaryConfig','LevelSequence','World']:
            if renderAsset.get_class().get_name() == 'MoviePipelinePrimaryConfig':
                MPPC_list.append( renderAsset.get_full_name() )
            elif renderAsset.get_class().get_name() == 'World':
                WD_list.append( renderAsset.get_name() )
            elif renderAsset.get_class().get_name() == 'LevelSequence':
                LS_list.append( str(renderAsset.get_full_name()) )
            else:
                pass                
            #print ( renderAsset.get_class().get_name() ,renderAsset.get_name() )

# 윈도우 생성
window = tk.Tk()
window.title(u"커멘드 렌더 Bat 파일 생성")
window.geometry("1000x250")
# 언리얼 프로젝트 내의 항목들
project_items = ['MoviePipelinePrimaryConfig', 'LevelSequence', 'World']

# MoviePipelinePrimaryConfig 셀렉트 박스 생성
movie_pipeline_primary_config_label = tk.Label(window, text="MoviePipelinePrimaryConfig")
movie_pipeline_primary_config_label.pack()
movie_pipeline_primary_config_combobox = ttk.Combobox(window, values=MPPC_list, state="readonly" , width=1000)
movie_pipeline_primary_config_combobox.pack()

# LevelSequence 셀렉트 박스 생성
level_sequence_label = tk.Label(window, text="LevelSequence")
level_sequence_label.pack()
level_sequence_combobox = ttk.Combobox(window, values=LS_list, state="readonly" , width=1000)
level_sequence_combobox.pack()

# World 셀렉트 박스 생성
world_label = tk.Label(window, text="World")
world_label.pack()
world_combobox = ttk.Combobox(window, values=WD_list, state="readonly", width=1000)
world_combobox.pack()

# 선택된 항목을 출력하는 버튼 생성
print_button = tk.Button(window, text="Print Selected Items", command=print_selected_items)
print_button.pack()

# 윈도우 실행
window.mainloop()
