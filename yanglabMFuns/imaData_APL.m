%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Class/Function 5: imaData_APL
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Written by Yang Zhang 20201-Dec-16
classdef imaData_APL < handle
    properties
        data        = [];
        TextureIdx  = -1; % index handle of the made texture
        filename    = ''; % filename the current image
        widNameIdx  = []; % indexes of widgetnames used the current image
        status      = []; %
    end
    
    methods
        function readIma(obj)
            if isempty(obj.data)
                % we already pre-generate a mat file for each image
%                obj.data   = imread(obj.filename);
                 tmp = load(obj.filename);
                 obj.data = tmp.data;
            end
        end

        function imSize = getImSize(obj)
           imSize = size(obj.data);
        end

        function initialStatus(obj)
            obj.status = false(numel(obj.widNameIdx),1);
        end

        function TextureIdx = makeTexture(obj, scrIdx, isPreload)
            if  isempty(obj.data)
                obj.readIma;
                TextureIdx = obj.makeTexture(scrIdx, isPreload);

            else
                if Screen(obj.TextureIdx,'WindowKind') % 0 for invalid, -1 for normal texture
                    TextureIdx = obj.TextureIdx;
                else
                    TextureIdx     = Screen('MakeTexture',scrIdx, obj.data);
                    obj.TextureIdx = TextureIdx;

                    if isPreload
                        resident = Screen('PreloadTextures', scrIdx, textureIdx);

                        if ~resident
                            error('gfx-hardware out of free video RAM memory!');
                        end
                    end
                end
            end
        end % end of subfun

        function excutiveClose(obj)
            Screen('Close',obj.TextureIdx);
            obj.TextureIdx = -1;
            obj.initialStatus;
            obj.data = [];
        end

        function closeTexture(obj, widNameIdx, closeMode)
            % closeMode: true, false for close directly, and close after all status values are true
            if obj.TextureIdx > 0
                [~, idx] = ismember(widNameIdx, obj.widNameIdx);
                obj.status(idx) = true;

                if closeMode
                    obj.excutiveClose;
                else
                    if all(obj.status)
                        obj.excutiveClose;
                    end
                end
            end

        end
        
    end % end of methods
end %  end of subfun5